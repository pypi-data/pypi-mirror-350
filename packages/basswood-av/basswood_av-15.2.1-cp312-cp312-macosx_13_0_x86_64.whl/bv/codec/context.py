from enum import Flag, IntEnum

import cython
from cython.cimports import libav as lib
from cython.cimports.bv.buffer import ByteSource, bytesource
from cython.cimports.bv.codec.codec import Codec, wrap_codec
from cython.cimports.bv.dictionary import _Dictionary
from cython.cimports.bv.error import err_check
from cython.cimports.bv.packet import Packet
from cython.cimports.bv.utils import avrational_to_fraction, to_avrational
from cython.cimports.libc.errno import EAGAIN
from cython.cimports.libc.stdint import uint8_t
from cython.cimports.libc.string import memcpy

from bv.dictionary import Dictionary

_cinit_sentinel = cython.declare(object, object())


@cython.cfunc
def wrap_codec_context(
    c_ctx: cython.pointer[lib.AVCodecContext],
    c_codec: cython.pointer[cython.const[lib.AVCodec]],
    hwaccel: HWAccel,
) -> CodecContext:
    """Build an bv.CodecContext for an existing AVCodecContext."""
    py_ctx: CodecContext

    if c_ctx.codec_type == lib.AVMEDIA_TYPE_VIDEO:
        from bv.video.codeccontext import VideoCodecContext

        py_ctx = VideoCodecContext(_cinit_sentinel)
    elif c_ctx.codec_type == lib.AVMEDIA_TYPE_AUDIO:
        from bv.audio.codeccontext import AudioCodecContext

        py_ctx = AudioCodecContext(_cinit_sentinel)
    elif c_ctx.codec_type == lib.AVMEDIA_TYPE_SUBTITLE:
        from bv.subtitles.codeccontext import SubtitleCodecContext

        py_ctx = SubtitleCodecContext(_cinit_sentinel)
    else:
        py_ctx = CodecContext(_cinit_sentinel)

    py_ctx._init(c_ctx, c_codec, hwaccel)

    return py_ctx


class ThreadType(Flag):
    NONE = 0
    FRAME: "Decode more than one frame at once" = lib.FF_THREAD_FRAME
    SLICE: "Decode more than one part of a single frame at once" = lib.FF_THREAD_SLICE
    AUTO: "Decode using both FRAME and SLICE methods." = (
        lib.FF_THREAD_SLICE | lib.FF_THREAD_FRAME
    )


class Flags(IntEnum):
    unaligned = lib.AV_CODEC_FLAG_UNALIGNED
    qscale = lib.AV_CODEC_FLAG_QSCALE
    four_mv = lib.AV_CODEC_FLAG_4MV
    output_corrupt = lib.AV_CODEC_FLAG_OUTPUT_CORRUPT
    qpel = lib.AV_CODEC_FLAG_QPEL
    drop_changed = 1 << 5
    recon_frame = lib.AV_CODEC_FLAG_RECON_FRAME
    copy_opaque = lib.AV_CODEC_FLAG_COPY_OPAQUE
    frame_duration = lib.AV_CODEC_FLAG_FRAME_DURATION
    pass1 = lib.AV_CODEC_FLAG_PASS1
    pass2 = lib.AV_CODEC_FLAG_PASS2
    loop_filter = lib.AV_CODEC_FLAG_LOOP_FILTER
    gray = lib.AV_CODEC_FLAG_GRAY
    psnr = lib.AV_CODEC_FLAG_PSNR
    interlaced_dct = lib.AV_CODEC_FLAG_INTERLACED_DCT
    low_delay = lib.AV_CODEC_FLAG_LOW_DELAY
    global_header = lib.AV_CODEC_FLAG_GLOBAL_HEADER
    bitexact = lib.AV_CODEC_FLAG_BITEXACT
    ac_pred = lib.AV_CODEC_FLAG_AC_PRED
    interlaced_me = lib.AV_CODEC_FLAG_INTERLACED_ME
    closed_gop = lib.AV_CODEC_FLAG_CLOSED_GOP


class Flags2(IntEnum):
    fast = lib.AV_CODEC_FLAG2_FAST
    no_output = lib.AV_CODEC_FLAG2_NO_OUTPUT
    local_header = lib.AV_CODEC_FLAG2_LOCAL_HEADER
    chunks = lib.AV_CODEC_FLAG2_CHUNKS
    ignore_crop = lib.AV_CODEC_FLAG2_IGNORE_CROP
    show_all = lib.AV_CODEC_FLAG2_SHOW_ALL
    export_mvs = lib.AV_CODEC_FLAG2_EXPORT_MVS
    skip_manual = lib.AV_CODEC_FLAG2_SKIP_MANUAL
    ro_flush_noop = lib.AV_CODEC_FLAG2_RO_FLUSH_NOOP


@cython.cclass
class CodecContext:
    @staticmethod
    def create(codec, mode=None, hwaccel=None):
        cy_codec: Codec = codec if isinstance(codec, Codec) else Codec(codec, mode)
        c_ctx: cython.pointer[lib.AVCodecContext] = lib.avcodec_alloc_context3(
            cy_codec.ptr
        )
        return wrap_codec_context(c_ctx, cy_codec.ptr, hwaccel)

    def __cinit__(self, sentinel=None, *args, **kwargs):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError("Cannot instantiate CodecContext")

        self.options = {}
        self.stream_index = -1  # This is set by the container immediately.
        self.is_open = False

    @cython.cfunc
    def _init(
        self,
        ptr: cython.pointer[lib.AVCodecContext],
        codec: cython.pointer[cython.const[lib.AVCodec]],
        hwaccel: HWAccel,
    ):
        self.ptr = ptr
        if self.ptr.codec and codec and self.ptr.codec != codec:
            raise RuntimeError("Wrapping CodecContext with mismatched codec.")
        self.codec = wrap_codec(codec if codec != cython.NULL else self.ptr.codec)
        self.hwaccel = hwaccel

        # Set reasonable threading defaults.
        self.ptr.thread_count = 0  # use as many threads as there are CPUs.
        self.ptr.thread_type = 0x02  # thread within a frame. Does not change the API.

    @property
    def flags(self):
        """
        Get and set the flags bitmask of CodecContext.

        :rtype: int
        """
        return self.ptr.flags

    @flags.setter
    def flags(self, value: cython.int):
        self.ptr.flags = value

    @property
    def qscale(self):
        """
        Use fixed qscale.

        :rtype: bool
        """
        return bool(self.ptr.flags & lib.AV_CODEC_FLAG_QSCALE)

    @qscale.setter
    def qscale(self, value):
        if value:
            self.ptr.flags |= lib.AV_CODEC_FLAG_QSCALE
        else:
            self.ptr.flags &= ~lib.AV_CODEC_FLAG_QSCALE

    @property
    def copy_opaque(self):
        return bool(self.ptr.flags & lib.AV_CODEC_FLAG_COPY_OPAQUE)

    @copy_opaque.setter
    def copy_opaque(self, value):
        if value:
            self.ptr.flags |= lib.AV_CODEC_FLAG_COPY_OPAQUE
        else:
            self.ptr.flags &= ~lib.AV_CODEC_FLAG_COPY_OPAQUE

    @property
    def flags2(self):
        """
        Get and set the flags2 bitmask of CodecContext.

        :rtype: int
        """
        return self.ptr.flags2

    @flags2.setter
    def flags2(self, value: cython.int):
        self.ptr.flags2 = value

    @property
    def extradata(self):
        if self.ptr is cython.NULL:
            return None
        if self.ptr.extradata_size > 0:
            return cython.cast(
                bytes,
                cython.cast(cython.pointer[uint8_t], self.ptr.extradata)[
                    : self.ptr.extradata_size
                ],
            )
        return None

    @extradata.setter
    def extradata(self, data):
        if data is None:
            lib.av_freep(cython.address(self.ptr.extradata))
            self.ptr.extradata_size = 0
        else:
            source = bytesource(data)
            self.ptr.extradata = cython.cast(
                cython.pointer[uint8_t],
                lib.av_realloc(
                    self.ptr.extradata, source.length + lib.AV_INPUT_BUFFER_PADDING_SIZE
                ),
            )
            if not self.ptr.extradata:
                raise MemoryError("Cannot allocate extradata")
            memcpy(self.ptr.extradata, source.ptr, source.length)
            self.ptr.extradata_size = source.length
        self.extradata_set = True

    @property
    def extradata_size(self):
        return self.ptr.extradata_size

    @property
    def is_encoder(self):
        if self.ptr is cython.NULL:
            return False
        return lib.av_codec_is_encoder(self.ptr.codec)

    @property
    def is_decoder(self):
        if self.ptr is cython.NULL:
            return False
        return lib.av_codec_is_decoder(self.ptr.codec)

    @cython.ccall
    def open(self, strict: cython.bint = True):
        if self.is_open:
            if strict:
                raise ValueError("CodecContext is already open.")
            return

        options: _Dictionary = Dictionary()
        options.update(self.options or {})

        if not self.ptr.time_base.num and self.is_encoder:
            if self.type == "video":
                self.ptr.time_base.num = self.ptr.framerate.den or 1
                self.ptr.time_base.den = self.ptr.framerate.num or lib.AV_TIME_BASE
            elif self.type == "audio":
                self.ptr.time_base.num = 1
                self.ptr.time_base.den = self.ptr.sample_rate
            else:
                self.ptr.time_base.num = 1
                self.ptr.time_base.den = lib.AV_TIME_BASE

        err_check(
            lib.avcodec_open2(self.ptr, self.codec.ptr, cython.address(options.ptr)),
            f'avcodec_open2("{self.codec.name}", {self.options})',
        )
        self.is_open = True
        self.options = dict(options)

    def __dealloc__(self):
        if self.ptr and self.extradata_set:
            lib.av_freep(cython.address(self.ptr.extradata))
        if self.ptr:
            lib.avcodec_free_context(cython.address(self.ptr))
        if self.parser:
            lib.av_parser_close(self.parser)

    def __repr__(self):
        _type = self.type or "<notype>"
        name = self.name or "<nocodec>"
        return f"<bv.{self.__class__.__name__} {_type}/{name} at 0x{id(self):x}>"

    def parse(self, raw_input=None):
        """Split up a byte stream into list of :class:`.Packet`.

        This is only effectively splitting up a byte stream, and does no
        actual interpretation of the data.

        It will return all packets that are fully contained within the given
        input, and will buffer partial packets until they are complete.

        :param ByteSource raw_input: A chunk of a byte-stream to process.
            Anything that can be turned into a :class:`.ByteSource` is fine.
            ``None`` or empty inputs will flush the parser's buffers.

        :return: ``list`` of :class:`.Packet` newly available.

        """

        if not self.parser:
            self.parser = lib.av_parser_init(self.codec.ptr.id)
            if not self.parser:
                raise ValueError(f"No parser for {self.codec.name}")

        source: ByteSource = bytesource(raw_input, allow_none=True)

        in_data: cython.p_uchar = source.ptr if source is not None else cython.NULL
        in_size: cython.int = source.length if source is not None else 0

        out_data: cython.p_uchar
        out_size: cython.int
        consumed: cython.int
        packet: Packet = None
        packets: list = []

        while True:
            with cython.nogil:
                consumed = lib.av_parser_parse2(
                    self.parser,
                    self.ptr,
                    cython.address(out_data),
                    cython.address(out_size),
                    in_data,
                    in_size,
                    lib.AV_NOPTS_VALUE,
                    lib.AV_NOPTS_VALUE,
                    0,
                )
            err_check(consumed)

            if out_size:
                # We copy the data immediately, as we have yet to figure out
                # the expected lifetime of the buffer we get back. All of the
                # examples decode it immediately.
                #
                # We've also tried:
                #   packet = Packet()
                #   packet.data = out_data
                #   packet.size = out_size
                #   packet.source = source
                #
                # ... but this results in corruption.

                packet = Packet(out_size)
                memcpy(packet.ptr.data, out_data, out_size)

                packets.append(packet)

            if not in_size:
                # This was a flush. Only one packet should ever be returned.
                break

            in_data += consumed
            in_size -= consumed

            if not in_size:
                break

        return packets

    @property
    def is_hwaccel(self):
        """
        Returns ``True`` if this codec context is hardware accelerated, ``False`` otherwise.
        """
        return self.hwaccel_ctx is not None

    def _send_frame_and_recv(self, frame: Frame | None):
        packet: Packet
        res: cython.int
        with cython.nogil:
            res = lib.avcodec_send_frame(
                self.ptr, frame.ptr if frame is not None else cython.NULL
            )
        err_check(res, "avcodec_send_frame()")

        packet = self._recv_packet()
        while packet:
            yield packet
            packet = self._recv_packet()

    @cython.cfunc
    def _send_packet_and_recv(self, packet: Packet | None):
        frame: Frame
        res: cython.int
        with cython.nogil:
            res = lib.avcodec_send_packet(
                self.ptr, packet.ptr if packet is not None else cython.NULL
            )
        err_check(res, "avcodec_send_packet()")

        out: list = []
        while True:
            frame = self._recv_frame()
            if frame:
                out.append(frame)
            else:
                break
        return out

    @cython.cfunc
    def _prepare_frames_for_encode(self, frame: Frame | None):
        return [frame]

    @cython.cfunc
    def _alloc_next_frame(self) -> Frame:
        raise NotImplementedError("Base CodecContext cannot decode.")

    @cython.cfunc
    def _recv_frame(self):
        if not self._next_frame:
            self._next_frame = self._alloc_next_frame()

        frame: Frame = self._next_frame
        res: cython.int

        with cython.nogil:
            res = lib.avcodec_receive_frame(self.ptr, frame.ptr)

        if res == -EAGAIN or res == lib.AVERROR_EOF:
            return

        err_check(res, "avcodec_receive_frame()")
        frame = self._transfer_hwframe(frame)

        if not res:
            self._next_frame = None
            return frame

    @cython.cfunc
    def _transfer_hwframe(self, frame: Frame):
        return frame

    @cython.cfunc
    def _recv_packet(self):
        packet: Packet = Packet()
        res: cython.int

        with cython.nogil:
            res = lib.avcodec_receive_packet(self.ptr, packet.ptr)

        if res == -EAGAIN or res == lib.AVERROR_EOF:
            return

        err_check(res, "avcodec_receive_packet()")
        if not res:
            return packet

    @cython.cfunc
    def _prepare_and_time_rebase_frames_for_encode(self, frame: Frame):
        if self.ptr.codec_type not in [lib.AVMEDIA_TYPE_VIDEO, lib.AVMEDIA_TYPE_AUDIO]:
            raise NotImplementedError("Encoding is only supported for audio and video.")

        self.open(strict=False)

        frames = self._prepare_frames_for_encode(frame)

        # Assert the frames are in our time base.
        # TODO: Don't mutate time.
        for frame in frames:
            if frame is not None:
                frame._rebase_time(self.ptr.time_base)

        return frames

    @cython.ccall
    def encode(self, frame: Frame | None = None):
        """Encode a list of :class:`.Packet` from the given :class:`.Frame`."""
        res = []
        for frame in self._prepare_and_time_rebase_frames_for_encode(frame):
            for packet in self._send_frame_and_recv(frame):
                self._setup_encoded_packet(packet)
                res.append(packet)
        return res

    def encode_lazy(self, frame: Frame | None = None):
        for frame in self._prepare_and_time_rebase_frames_for_encode(frame):
            for packet in self._send_frame_and_recv(frame):
                self._setup_encoded_packet(packet)
                yield packet

    @cython.cfunc
    def _setup_encoded_packet(self, packet: Packet):
        # We coerced the frame's time_base into the CodecContext's during encoding,
        # and FFmpeg copied the frame's pts/dts to the packet, so keep track of
        # this time_base in case the frame needs to be muxed to a container with
        # a different time_base.
        #
        # NOTE: if the CodecContext's time_base is altered during encoding, all bets
        # are off!
        packet._time_base = self.ptr.time_base

    @cython.ccall
    def decode(self, packet: Packet | None = None):
        """Decode a list of :class:`.Frame` from the given :class:`.Packet`.

        If the packet is None, the buffers will be flushed. This is useful if
        you do not want the library to automatically re-order frames for you
        (if they are encoded with a codec that has B-frames).

        """
        if not self.codec.ptr:
            raise ValueError("cannot decode unknown codec")

        self.open(strict=False)

        res: list = []
        for frame in self._send_packet_and_recv(packet):
            if isinstance(frame, Frame):
                self._setup_decoded_frame(frame, packet)
            res.append(frame)
        return res

    @cython.ccall
    def flush_buffers(self):
        """Reset the internal codec state and discard all internal buffers.

        Should be called before you start decoding from a new position e.g.
        when seeking or when switching to a different stream.

        """
        if self.is_open:
            with cython.nogil:
                lib.avcodec_flush_buffers(self.ptr)

    @cython.cfunc
    def _setup_decoded_frame(self, frame: Frame, packet: Packet | None):
        # Propagate our manual times.
        # While decoding, frame times are in stream time_base, which PyAV
        # is carrying around.
        # TODO: Somehow get this from the stream so we can not pass the
        # packet here (because flushing packets are bogus).
        if packet is not None:
            frame._time_base = packet._time_base

    @property
    def name(self):
        return self.codec.name

    @property
    def type(self):
        return self.codec.type

    @property
    def profiles(self):
        """
        List the available profiles for this stream.

        :type: list[str]
        """
        ret: list = []
        if not self.ptr.codec or not self.codec.desc or not self.codec.desc.profiles:
            return ret

        # Profiles are always listed in the codec descriptor, but not necessarily in
        # the codec itself. So use the descriptor here.
        desc = self.codec.desc
        i: cython.int = 0
        while desc.profiles[i].profile != lib.FF_PROFILE_UNKNOWN:
            ret.append(desc.profiles[i].name)
            i += 1

        return ret

    @property
    def profile(self):
        if not self.ptr.codec or not self.codec.desc or not self.codec.desc.profiles:
            return

        # Profiles are always listed in the codec descriptor, but not necessarily in
        # the codec itself. So use the descriptor here.
        desc = self.codec.desc
        i: cython.int = 0
        while desc.profiles[i].profile != lib.FF_PROFILE_UNKNOWN:
            if desc.profiles[i].profile == self.ptr.profile:
                return desc.profiles[i].name
            i += 1

    @profile.setter
    def profile(self, value):
        if not self.codec or not self.codec.desc or not self.codec.desc.profiles:
            return

        # Profiles are always listed in the codec descriptor, but not necessarily in
        # the codec itself. So use the descriptor here.
        desc = self.codec.desc
        i: cython.int = 0
        while desc.profiles[i].profile != lib.FF_PROFILE_UNKNOWN:
            if desc.profiles[i].name == value:
                self.ptr.profile = desc.profiles[i].profile
                return
            i += 1

    @property
    def time_base(self):
        if self.is_decoder:
            raise RuntimeError("Cannot access 'time_base' as a decoder")
        return avrational_to_fraction(cython.address(self.ptr.time_base))

    @time_base.setter
    def time_base(self, value):
        if self.is_decoder:
            raise RuntimeError("Cannot access 'time_base' as a decoder")
        to_avrational(value, cython.address(self.ptr.time_base))

    @property
    def codec_tag(self):
        return self.ptr.codec_tag.to_bytes(4, byteorder="little", signed=False).decode(
            encoding="ascii"
        )

    @codec_tag.setter
    def codec_tag(self, value):
        if isinstance(value, str) and len(value) == 4:
            self.ptr.codec_tag = int.from_bytes(
                value.encode(encoding="ascii"), byteorder="little", signed=False
            )
        else:
            raise ValueError("Codec tag should be a 4 character string.")

    @property
    def bit_rate(self):
        return self.ptr.bit_rate if self.ptr.bit_rate > 0 else None

    @bit_rate.setter
    def bit_rate(self, value: cython.int):
        self.ptr.bit_rate = value

    @property
    def max_bit_rate(self):
        if self.ptr.rc_max_rate > 0:
            return self.ptr.rc_max_rate
        else:
            return None

    @property
    def bit_rate_tolerance(self):
        self.ptr.bit_rate_tolerance

    @bit_rate_tolerance.setter
    def bit_rate_tolerance(self, value: cython.int):
        self.ptr.bit_rate_tolerance = value

    @property
    def thread_count(self):
        """How many threads to use; 0 means auto.

        Wraps :ffmpeg:`AVCodecContext.thread_count`.

        """
        return self.ptr.thread_count

    @thread_count.setter
    def thread_count(self, value: cython.int):
        if self.is_open:
            raise RuntimeError("Cannot change thread_count after codec is open.")
        self.ptr.thread_count = value

    @property
    def thread_type(self):
        """One of :class:`.ThreadType`.

        Wraps :ffmpeg:`AVCodecContext.thread_type`.

        """
        return ThreadType(self.ptr.thread_type)

    @thread_type.setter
    def thread_type(self, value):
        if self.is_open:
            raise RuntimeError("Cannot change thread_type after codec is open.")
        if type(value) is int:
            self.ptr.thread_type = value
        elif type(value) is str:
            self.ptr.thread_type = ThreadType[value].value
        else:
            self.ptr.thread_type = value.value

    @property
    def skip_frame(self):
        """Returns one of the following str literals:

        "NONE" Discard nothing
        "DEFAULT" Discard useless packets like 0 size packets in AVI
        "NONREF" Discard all non reference
        "BIDIR" Discard all bidirectional frames
        "NONINTRA" Discard all non intra frames
        "NONKEY Discard all frames except keyframes
        "ALL" Discard all

        Wraps :ffmpeg:`AVCodecContext.skip_frame`.
        """
        value = self.ptr.skip_frame
        if value == lib.AVDISCARD_NONE:
            return "NONE"
        if value == lib.AVDISCARD_DEFAULT:
            return "DEFAULT"
        if value == lib.AVDISCARD_NONREF:
            return "NONREF"
        if value == lib.AVDISCARD_BIDIR:
            return "BIDIR"
        if value == lib.AVDISCARD_NONINTRA:
            return "NONINTRA"
        if value == lib.AVDISCARD_NONKEY:
            return "NONKEY"
        if value == lib.AVDISCARD_ALL:
            return "ALL"
        return f"{value}"

    @skip_frame.setter
    def skip_frame(self, value):
        if value == "NONE":
            self.ptr.skip_frame = lib.AVDISCARD_NONE
        elif value == "DEFAULT":
            self.ptr.skip_frame = lib.AVDISCARD_DEFAULT
        elif value == "NONREF":
            self.ptr.skip_frame = lib.AVDISCARD_NONREF
        elif value == "BIDIR":
            self.ptr.skip_frame = lib.AVDISCARD_BIDIR
        elif value == "NONINTRA":
            self.ptr.skip_frame = lib.AVDISCARD_NONINTRA
        elif value == "NONKEY":
            self.ptr.skip_frame = lib.AVDISCARD_NONKEY
        elif value == "ALL":
            self.ptr.skip_frame = lib.AVDISCARD_ALL
        else:
            raise ValueError("Invalid skip_frame type")

    @property
    def delay(self):
        """Codec delay.

        Wraps :ffmpeg:`AVCodecContext.delay`.

        """
        return self.ptr.delay
