// Copyright 2013 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package japanese

import (
	"unicode/utf8"

	"golang.org/x/text/encoding"
	"golang.org/x/text/transform"

	"gitlab.com/HiSakDev/go-encoding/internal"
	"gitlab.com/HiSakDev/go-encoding/internal/identifier"
)

// CP932 is the Code Page 932 encoding, also known as Windows-31J.
var CP932 encoding.Encoding = &cp932

var cp932 = internal.Encoding{
	Encoding: &internal.SimpleEncoding{
		Decoder: cp932Decoder{},
		Encoder: cp932Encoder{},
	},
	Name: "CP932",
	MIB:  identifier.Windows31J,
}

type cp932Decoder struct{ transform.NopResetter }

func (cp932Decoder) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error) {
	r, size := rune(0), 0
loop:
	for ; nSrc < len(src); nSrc += size {
		switch c0 := src[nSrc]; {
		case c0 < utf8.RuneSelf:
			r, size = rune(c0), 1

		case 0xa1 <= c0 && c0 < 0xe0:
			r, size = rune(c0)+(0xff61-0xa1), 1

		case (0x81 <= c0 && c0 < 0xa0) || (0xe0 <= c0 && c0 < 0xfd):
			if nSrc+1 >= len(src) {
				if !atEOF {
					err = transform.ErrShortSrc
					break loop
				}
				r, size = '\ufffd', 1
				goto write
			}
			c1 := src[nSrc+1]

			if 0xf0 <= c0 && c0 <= 0xf9 {
				if v1 := int(c1 - 0x40); v1 != 63 && v1 <= 188 {
					if v1 >= 0x40 {
						v1--
					}
					r, size = rune(0xE000+int(c0-0xf0)*188+v1), 2
					if r == 0 {
						r = utf8.RuneError
					}
				} else {
					r, size = utf8.RuneError, 1
				}
				goto write
			}

			if c0 <= 0x9f {
				c0 -= 0x70
			} else {
				c0 -= 0xb0
			}
			c0 = 2*c0 - 0x21
			switch {
			case c1 < 0x40:
				r, size = '\ufffd', 1 // c1 is ASCII so output on next round
				goto write
			case c1 < 0x7f:
				c0--
				c1 -= 0x40
			case c1 == 0x7f:
				r, size = '\ufffd', 1 // c1 is ASCII so output on next round
				goto write
			case c1 < 0x9f:
				c0--
				c1 -= 0x41
			case c1 < 0xfd:
				c1 -= 0x9f
			default:
				r, size = '\ufffd', 2
				goto write
			}
			r, size = '\ufffd', 2
			if i := int(c0)*94 + int(c1); i < len(jis0208Decode) {
				r = rune(jis0208Decode[i])
				if r == 0 {
					r = '\ufffd'
				}
			}

		case c0 == 0x80:
			r, size = 0x80, 1

		case c0 == 0xa0:
			r, size = 0xF8F0, 1

		case c0 == 0xfd:
			r, size = 0xF8F1, 1

		case c0 == 0xfe:
			r, size = 0xF8F2, 1

		case c0 == 0xff:
			r, size = 0xF8F3, 1

		default:
			r, size = '\ufffd', 1
		}
	write:
		if nDst+utf8.RuneLen(r) > len(dst) {
			err = transform.ErrShortDst
			break loop
		}
		nDst += utf8.EncodeRune(dst[nDst:], r)
	}
	return nDst, nSrc, err
}

type cp932Encoder struct{ transform.NopResetter }

func (cp932Encoder) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error) {
	r, size := rune(0), 0
loop:
	for ; nSrc < len(src); nSrc += size {
		r = rune(src[nSrc])

		// Decode a 1-byte rune.
		if r < utf8.RuneSelf {
			size = 1

		} else {
			// Decode a multi-byte rune.
			r, size = utf8.DecodeRune(src[nSrc:])
			if size == 1 {
				// All valid runes of size 1 (those below utf8.RuneSelf) were
				// handled above. We have invalid UTF-8 or we haven't seen the
				// full character yet.
				if !atEOF && !utf8.FullRune(src[nSrc:]) {
					err = transform.ErrShortSrc
					break loop
				}
			}

			if r == 0x80 {
				goto write1
			} else if 0xA1 <= r && r <= 0xFF {
				// codepage many to one
				if v := rune(codepageManyToOneEncode0[r]); v != 0 {
					r = v
					if r <= 0xFF {
						goto write1
					}
				}
			} else if r == 0x3094 {
				// codepage many to one
				r = 0x30F4
			}

			// func init checks that the switch covers all tables.
			switch {
			case encode0Low <= r && r < encode0High:
				if r < rune(len(cp932Encode0)) {
					if v := rune(cp932Encode0[r]); v != 0 {
						r = v
						goto write2ext
					}
				}
				if r = rune(encode0[r-encode0Low]); r>>tableShift == jis0208 {
					goto write2
				}
			case encode1Low <= r && r < encode1High:
				if 0x2170 <= r && r <= 0x2179 {
					r += 0xFA40 - 0x2170
					goto write2ext
				}
				if r = rune(encode1[r-encode1Low]); r>>tableShift == jis0208 {
					goto write2
				}
			case encode2Low <= r && r < encode2High:
				if r = rune(encode2[r-encode2Low]); r>>tableShift == jis0208 {
					goto write2
				}
			case encode3Low <= r && r < encode3High:
				if r = rune(encode3[r-encode3Low]); r>>tableShift == jis0208 {
					goto write2
				}
			case encode4Low <= r && r < encode4High:
				if r < rune(len(cp932Encode1)) {
					if v := rune(cp932Encode1[r]); v != 0 {
						r = v
						goto write2ext
					}
				}
				if r = rune(encode4[r-encode4Low]); r>>tableShift == jis0208 {
					goto write2
				}
			case encode5Low <= r && r < encode5High:
				switch {
				case 0xFF61 <= r && r <= 0xFF9F:
					r -= 0xFF61 - 0xA1
					goto write1
				case r == 0xFF02:
					r = 0xFA57
					goto write2ext
				case r == 0xFF07:
					r = 0xFA56
					goto write2ext
				case r == 0xFFE4:
					r = 0xFA55
					goto write2ext
				}
				if r = rune(encode5[r-encode5Low]); r>>tableShift == jis0208 {
					goto write2
				}
			}

			switch {
			case 0xE000 <= r && r <= 0xE757:
				r = r & 0x1FFF
				goto private2
			case r == 0xF8F0:
				r = 0xA0
				goto write1
			case r == 0xF8F1:
				r = 0xFD
				goto write1
			case r == 0xF8F2:
				r = 0xFE
				goto write1
			case r == 0xF8F3:
				r = 0xFF
				goto write1
			}

			err = cp932Replacement
			break
		}

	write1:
		if nDst >= len(dst) {
			err = transform.ErrShortDst
			break
		}
		dst[nDst] = uint8(r)
		nDst++
		continue

	write2ext:
		if nDst+2 > len(dst) {
			err = transform.ErrShortDst
			break
		}
		dst[nDst+0] = uint8((r >> 8) & 0xff)
		dst[nDst+1] = uint8(r & 0xff)
		nDst += 2
		continue

	private2:
		if nDst+2 > len(dst) {
			err = transform.ErrShortDst
			break
		}
		dst[nDst+0] = 0xf0 + byte(r/188)
		if v := byte(r % 188); v < 63 {
			dst[nDst+1] = 0x40 + v
		} else {
			dst[nDst+1] = 0x80 + v - 63
		}
		nDst += 2
		continue

	write2:
		j1 := uint8(r>>codeShift) & codeMask
		j2 := uint8(r) & codeMask
		if nDst+2 > len(dst) {
			err = transform.ErrShortDst
			break loop
		}
		if j1 <= 61 {
			dst[nDst+0] = 129 + j1/2
		} else {
			dst[nDst+0] = 193 + j1/2
		}
		if j1&1 == 0 {
			dst[nDst+1] = j2 + j2/63 + 64
		} else {
			dst[nDst+1] = j2 + 159
		}
		nDst += 2
		continue
	}
	return nDst, nSrc, err
}
