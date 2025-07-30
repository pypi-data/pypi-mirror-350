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

// EUCJPMS is the EUC-JP-MS encoding.
var EUCJPMS encoding.Encoding = &eucJPms

var eucJPms = internal.Encoding{
	Encoding: &internal.SimpleEncoding{
		Decoder: eucJPmsDecoder{},
		Encoder: eucJPmsEncoder{},
	},
	Name: "EUC-JP-MS",
	MIB:  identifier.EUCPkdFmtJapanese,
}

type eucJPmsDecoder struct{ transform.NopResetter }

func (eucJPmsDecoder) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error) {
	r, size := rune(0), 0
loop:
	for ; nSrc < len(src); nSrc += size {
		switch c0 := src[nSrc]; {
		case 0x80 <= c0 && c0 <= 0x8d:
			fallthrough

		case 0x90 <= c0 && c0 <= 0x9f:
			fallthrough

		case c0 < utf8.RuneSelf:
			r, size = rune(c0), 1

		case c0 == 0x8e:
			if nSrc+1 >= len(src) {
				if !atEOF {
					err = transform.ErrShortSrc
					break loop
				}
				r, size = utf8.RuneError, 1
				break
			}
			c1 := src[nSrc+1]
			switch {
			case c1 < 0xa1:
				r, size = utf8.RuneError, 1
			case c1 > 0xdf:
				r, size = utf8.RuneError, 2
				if c1 == 0xff {
					size = 1
				}
			default:
				r, size = rune(c1)+(0xff61-0xa1), 2
			}
		case c0 == 0x8f:
			if nSrc+2 >= len(src) {
				if !atEOF {
					err = transform.ErrShortSrc
					break loop
				}
				r, size = utf8.RuneError, 1
				if p := nSrc + 1; p < len(src) && 0xa1 <= src[p] && src[p] < 0xfe {
					size = 2
				}
				break
			}
			c1 := src[nSrc+1]
			if c1 < 0xa1 || 0xfe < c1 {
				r, size = utf8.RuneError, 1
				break
			}
			c2 := src[nSrc+2]
			if c2 < 0xa1 || 0xfe < c2 {
				r, size = utf8.RuneError, 2
				break
			}
			r, size = utf8.RuneError, 3
			if c1 < 0xf3 {
				if i := int(c1-0xa1)*94 + int(c2-0xa1); i < len(jis0212Decode) {
					if i == 128 {
						r = 0xFFE4
					} else {
						r = rune(jis0212Decode[i])
					}
					if r == 0 {
						r = utf8.RuneError
					}
				}
			} else if c1 <= 0xf4 {
				if i := int(c1-0xa1)*94 + int(c2-0xa1); i < len(eucJPmsIBMExtDecode) {
					r = rune(eucJPmsIBMExtDecode[i])
					if r == 0 {
						r = utf8.RuneError
					}
				}
			} else {
				if i := int(c1-0xf5)*94 + int(c2-0xa1); i < 8836 {
					r = rune(0xE3AC + i)
					if r == 0 {
						r = utf8.RuneError
					}
				}
			}

		case 0xa1 <= c0 && c0 <= 0xfe:
			if nSrc+1 >= len(src) {
				if !atEOF {
					err = transform.ErrShortSrc
					break loop
				}
				r, size = utf8.RuneError, 1
				break
			}
			c1 := src[nSrc+1]
			if c1 < 0xa1 || 0xfe < c1 {
				r, size = utf8.RuneError, 1
				break
			}
			r, size = utf8.RuneError, 2
			if c0 < 0xf5 {
				if i := int(c0-0xa1)*94 + int(c1-0xa1); i < len(jis0208Decode) {
					r = rune(jis0208Decode[i])
					if r == 0 {
						r = utf8.RuneError
					}
				}
			} else {
				if i := int(c0-0xf5)*94 + int(c1-0xa1); i < 8836 {
					r = rune(0xE000 + i)
					if r == 0 {
						r = utf8.RuneError
					}
				}
			}

		default:
			r, size = utf8.RuneError, 1
		}

		if nDst+utf8.RuneLen(r) > len(dst) {
			err = transform.ErrShortDst
			break loop
		}
		nDst += utf8.EncodeRune(dst[nDst:], r)
	}
	return nDst, nSrc, err
}

type eucJPmsEncoder struct{ transform.NopResetter }

func (eucJPmsEncoder) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error) {
	r, size := rune(0), 0
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
					break
				}
			}

			if r < rune(len(eucJPmsIBMExtEncode)) {
				if v := eucJPmsIBMExtEncode[r]; v != 0 {
					if nDst+3 > len(dst) {
						err = transform.ErrShortDst
						break
					}
					dst[nDst+0] = 0x8f
					dst[nDst+1] = 0xf3 + byte(v/94)
					dst[nDst+2] = 0xa1 + byte(v%94)
					nDst += 3
					continue
				}
			}
			if r < rune(len(eucJPmsJIS0212Encode)) {
				if v := eucJPmsJIS0212Encode[r]; v != 0 {
					if nDst+3 > len(dst) {
						err = transform.ErrShortDst
						break
					}
					dst[nDst+0] = 0x8f
					dst[nDst+1] = byte((v >> 8) & 0xff)
					dst[nDst+2] = byte(v & 0xff)
					nDst += 3
					continue
				}
			}
			switch r {
			case 0x00A2:
				r = 0xA1F1
				goto write1or2ext
			case 0x00A3:
				r = 0xA1F2
				goto write1or2ext
			case 0x00A5:
				r = 0x5C
				goto write1or2ext
			case 0x00AC:
				r = 0xA2CC
				goto write1or2ext
			case 0x2014:
				r = 0xA1BD
				goto write1or2ext
			case 0x2016:
				r = 0xA1C2
				goto write1or2ext
			case 0x203E:
				r = 0x7E
				goto write1or2ext
			case 0x2212:
				r = 0xA1DD
				goto write1or2ext
			case 0x301C:
				r = 0xA1C1
				goto write1or2ext
			}

			// func init checks that the switch covers all tables.
			switch {
			case 0x80 <= r && r <= 0x8d:
				goto write1
			case 0x90 <= r && r <= 0x9f:
				goto write1
			case encode0Low <= r && r < encode0High:
				if r = rune(encode0[r-encode0Low]); r != 0 {
					goto write2or3
				}
			case encode1Low <= r && r < encode1High:
				if r = rune(encode1[r-encode1Low]); r != 0 {
					goto write2or3
				}
			case encode2Low <= r && r < encode2High:
				if r = rune(encode2[r-encode2Low]); r != 0 {
					goto write2or3
				}
			case encode3Low <= r && r < encode3High:
				if r = rune(encode3[r-encode3Low]); r != 0 {
					goto write2or3
				}
			case encode4Low <= r && r < encode4High:
				if r = rune(encode4[r-encode4Low]); r != 0 {
					goto write2or3
				}
			case encode5Low <= r && r < encode5High:
				if 0xff61 <= r && r < 0xffa0 {
					goto write2
				}
				if r = rune(encode5[r-encode5Low]); r != 0 {
					goto write2or3
				}
			}
			if 0xE000 <= r && r <= 0xE757 {
				r = r & 0x1FFF
				goto private2or3
			}
			err = eucJPmsReplacement
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

	write1or2ext:
		if r <= 0xff {
			if nDst >= len(dst) {
				err = transform.ErrShortDst
				break
			}
		} else {
			if nDst+2 > len(dst) {
				err = transform.ErrShortDst
				break
			}
			dst[nDst] = byte((r >> 8) & 0xff)
			nDst++
		}
		dst[nDst] = byte(r & 0xff)
		nDst++
		continue

	private2or3:
		if r < 940 {
			if nDst+2 > len(dst) {
				err = transform.ErrShortDst
				break
			}
		} else {
			if nDst+3 > len(dst) {
				err = transform.ErrShortDst
				break
			}
			dst[nDst] = 0x8f
			nDst++
			r -= 940
		}
		dst[nDst+0] = 0xf5 + byte(r/94)
		dst[nDst+1] = 0xa1 + byte(r%94)
		nDst += 2
		continue

	write2or3:
		if r>>tableShift == jis0208 {
			if nDst+2 > len(dst) {
				err = transform.ErrShortDst
				break
			}
		} else {
			if nDst+3 > len(dst) {
				err = transform.ErrShortDst
				break
			}
			dst[nDst] = 0x8f
			nDst++
		}
		dst[nDst+0] = 0xa1 + uint8(r>>codeShift)&codeMask
		dst[nDst+1] = 0xa1 + uint8(r)&codeMask
		nDst += 2
		continue

	write2:
		if nDst+2 > len(dst) {
			err = transform.ErrShortDst
			break
		}
		dst[nDst+0] = 0x8e
		dst[nDst+1] = uint8(r - (0xff61 - 0xa1))
		nDst += 2
		continue
	}
	return nDst, nSrc, err
}
