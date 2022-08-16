from itertools import combinations

alterations = ['b5', '#5', 'b9', '#9', '#11', 'b13']
bases = [7, 9, 13]
triangle_names = ['t', '^']
base = 'm:0:-&extup; e{ext} m:0:&extup;'
triangle = 'm:0:-&modup; triangle m:0:&modup;'
st2indent = '&st2ind;'
st3indent = '&st3ind;'
st2template = 'm:&stpad;:&st2down; ss( m:&br2pad;:-&st2baseline; :push m:{alt1indent}:&st2halflineh; {alt1} :pop ' \
			'm:0:-&st2halflineh; {alt2} m:0:&st2halflineh; m:&br2pad;:&st2baseline; ss) m:0:-&st2down; '
st3template = 'm:&stpad;:&st3down; sss( m:&br3pad;:-&st3baseline; :push m:{alt1indent}:&st3lineh; {alt1} :pop :push ' \
			'm:{alt2indent}:0 {alt2} :pop m:0:-&st3lineh; {alt3} m:0:&st3lineh; m:&br3pad;:&st3baseline; sss) ' \
			'm:0:-&st3down; '
st4template = 'm:&stpad;:&st2down; ss( m:&br2pad;:-&st2baseline; :push m:{alt1indent}:&st2halflineh; {alt1} :pop  ' \
			'm:0:-&st2halflineh; {alt2} m:0:&st2halflineh; m:&st4pad;:0 :push m:{alt3indent}:&st2halflineh; {alt3} ' \
			':pop m:0:-&st2halflineh; {alt4} m:0:&st2halflineh; m:&br2pad;:&st2baseline; ss) m:0:-&st2down; '
nametemplate = '\t<name>{name}</name>\n'
chordtemplate = '<chord>\n{names}\t<render>{render}</render>\n</chord>'


def write_alt(alt, stacked=2):
	prefix = stacked * 's'
	accidental = alt[:1]
	move = '&sharpind;'
	if accidental == 'b':
		move = '&flatind;'
	return f"m:{move}:0 {prefix}{accidental} {prefix}{alt[1:]}"


def write_chords():
	result = ''
	for chord in generate_chords():
		names_list = chord_names(chord)
		names = ''.join([nametemplate.format(name=name) for name in names_list])
		render = ''
		if chord['triangle']:
			render = triangle + ' '
		render += base.format(ext=chord['base']) + ' '

		alts = chord['alts']
		if len(alts) == 2:
			indent = 0
			if len(alts[0]) == 2 and len(alts[1]) == 3:
				indent = st2indent
			render += st2template.format(
				alt1=write_alt(alts[0]),
				alt2=write_alt(alts[1]),
				alt1indent=indent
			)
		elif len(alts) == 3:
			indent1 = indent2 = 0
			if len(alts[2]) == 3:
				if len(alts[0]) == 2:
					indent1 = st3indent
				if len(alts[1]) == 2:
					indent2 = st3indent
			render += st3template.format(
				alt1=write_alt(alts[0]),
				alt2=write_alt(alts[1]),
				alt3=write_alt(alts[2]),
				alt1indent=indent1,
				alt2indent=indent2
			)
		elif len(alts) == 4:
			indent1 = indent3 = 0
			if len(alts[0]) == 2 and len(alts[1]) == 3:
				indent1 = st2indent
			if len(alts[2]) == 2 and len(alts[3]) == 3:
				indent3 = st2indent
			render += st4template.format(
				alt1=write_alt(alts[0]),
				alt2=write_alt(alts[1]),
				alt3=write_alt(alts[2]),
				alt4=write_alt(alts[3]),
				alt1indent=indent1,
				alt3indent=indent3
			)
		result += chordtemplate.format(names=names, render=render) + '\n'

	return result


def generate_chords():
	chords = []
	for n in (2, 3, 4):
		alts = combinations(alterations, n)
		for chord in alts:
			if 'b5' in chord and '#11' in chord or '#5' in chord and 'b13' in chord:
				continue

			for bs in bases:
				if f'b{bs}' in chord or f'#{bs}' in chord:
					continue
				for tr in (True, False):
					chords.append({'base': bs, 'triangle': tr, 'alts': chord})
	return chords


def chord_names(chord):
	if chord['triangle']:
		return [f"{tr}{chord['base']}({''.join(chord['alts'])})" for tr in triangle_names]
	return [f"{chord['base']}({''.join(chord['alts'])})"]


def main():
	print('Generate XML for custom chords...')
	xml = write_chords()

	print('Write XML to chords_extended.xml...')
	with open('templates/chords_template.xml', 'r') as template, open('chords_extended.xml', 'w') as output:
		output.write(template.read().replace('!chords!', xml, 1))

	print('Write XML to chords_extended_jazz.xml...')
	with open('templates/chords_template_jazz.xml', 'r') as template, open('chords_extended_jazz.xml', 'w') as output:
		output.write(template.read().replace('!chords!', xml, 1))

	print('Done.')


if __name__ == '__main__':
	main()
