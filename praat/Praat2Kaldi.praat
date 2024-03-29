##############################################################
## TextGrid to Kaldi 
##############################################################
## This script:
# 1) Takes one set of anotated TextGrid with two text grids
#	- One for syllables (tier 1): separated with spaces. For example, "mesa" should be written me sa"
#	- One for phonemes (tier 2): identical to tier one, but phonemes are "_" separated within syllables. For example: "m_e s_a" 
# 2) converts them to Kaldi sement format and saves in PATHOUT

# To run the script: select the TextGrids and run the script
# One segment file will be generated per TextGrid

# Choose the location


#pathOut$ = "/Users/ignaciomoreno-torres/Library/Mobile Documents/com~apple~CloudDocs/Invest/ASICA/⁨DataASICACrista⁩/Controles⁩/data⁩/"
#pathOut$ = "/Users/imt/Library/Mobile Documents/com~apple~CloudDocs/Invest/ASICA/⁨DataASICACrista⁩/Controles⁩/data⁩/"
#pathOut$ = "/Users/ignaciomoreno-torres/Desktop/kaldi-master/egs/ASICAKaldiRecipe/info_user/"
pathOut$ = "⁩⁨⁩⁩⁩⁩⁩⁩"



# Tier that will be used. Tier 1: Silables; Tier2: Phonemes
	tier1 = 1 
	tier2 = 2 

n = numberOfSelected ("TextGrid")


# Column headers
	appendInfoLine: "Start  	End 	Silable	Phonemes"

for i to n 
	textG'i' = selected ("TextGrid", i)
	textG'i'$ = selected$("TextGrid", i)
endfor

# Main loop for the different textGrids

for i to n
	objeto$ = textG'i'$
    selectObject: "TextGrid 'objeto$'"
	 workingTextGrid$ = selected$ ("TextGrid")

# Guardo el TextGrid
 	cadenaTextGrid$ = pathOut$ + workingTextGrid$ + ".TextGrid"
 	Save as text file: cadenaTextGrid$

	number_of_intervals = Get number of intervals... tier1


# Loop for the intervals in the Textgrid

clearinfo

for int from 1 to number_of_intervals

	select TextGrid 'workingTextGrid$'

# Gets starting point
	begin = Get starting point... tier1 int

# Gets end point	
	end = Get end point... tier1 int

# Gets label 
	silabas$ = Get label of interval... tier1 int
	fonemas$ = Get label of interval... tier2 int

if silabas$ <> ""
	appendInfo: begin		
	appendInfo: "	"
	appendInfo: end	
	appendInfo: "	"
	appendInfo: silabas$
	appendInfo: "	"
	appendInfoLine: fonemas$
endif

endfor

filename$ = pathOut$ + workingTextGrid$+".kal"
writeFile: filename$, info$ ( )


endfor # Main loop

