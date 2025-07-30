package japanese

import (
	"golang.org/x/text/encoding"

	"gitlab.com/HiSakDev/go-encoding/internal"
)

var (
	cp932Replacement     = internal.ErrASCIIReplacement
	cp51932Replacement   = internal.ErrASCIIReplacement
	eucJPmsReplacement   = internal.ErrASCIIReplacement
	eucJPReplacement     = internal.ErrASCIIReplacement
	iso2022JPReplacement = internal.ErrASCIIReplacement
	shiftJISReplacement  = internal.ErrASCIIReplacement
)

func SetReplacement(enc encoding.Encoding, char byte) {
	switch enc {
	case &cp932:
		cp932Replacement = internal.RepertoireError(char)
	case &cp51932:
		cp51932Replacement = internal.RepertoireError(char)
	case &eucJPms:
		eucJPmsReplacement = internal.RepertoireError(char)
	case &eucJP:
		eucJPReplacement = internal.RepertoireError(char)
	case &iso2022JP:
		iso2022JPReplacement = internal.RepertoireError(char)
	case &shiftJIS:
		shiftJISReplacement = internal.RepertoireError(char)
	}
}
