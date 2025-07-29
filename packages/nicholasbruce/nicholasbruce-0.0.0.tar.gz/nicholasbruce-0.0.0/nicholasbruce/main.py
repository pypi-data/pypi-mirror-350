from termcolor import colored
import re


def main():
    def hex_to_ansi(hex_color):
        return tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

    # Define colors and styles (Base4Tone Classic C)
    def border(x): return colored(x, hex_to_ansi('#1ABC9C'))
    def divider(x): return colored(x, hex_to_ansi('#7F8C8D'))
    def plain_text(x): return colored(x, hex_to_ansi('#FFFFFF'))
    def secondary(x): return colored(x, hex_to_ansi('#C0392B'))
    def highlight(x): return colored(x, hex_to_ansi('#FDBC4B'), attrs=['bold'])
    def handle(x): return colored(x, hex_to_ansi('#16A085'))
    def label(x): return colored(x, hex_to_ansi('#1D99F3'), attrs=['bold'])
    def bsky(x): return colored(x, hex_to_ansi('#3DAEE9'))
    def url(x): return colored(x, hex_to_ansi('#55A649'), attrs=['underline'])
    def email(x): return colored(x, hex_to_ansi('#9B59B6'))
    def gh(x): return colored(x, hex_to_ansi('#FDBC4B'))
    def work(x): return colored(x, hex_to_ansi('#ED1515'))

    flag = '🇨🇦'
    # Card dimensions - fixed width for better alignment
    width = 57

    # Create borders with exact width
    top_border = border('╭' + '─' * width + '╮')
    bottom_border = border('╰' + '─' * width + '╯')

    def strip_ansi_codes(text):
        ansi_escape_pattern = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape_pattern.sub('', text)

    # Function to create a line with perfectly aligned borders
    def create_line(text: str):
        # Strip ANSI codes for accurate length calculation
        clean_text = strip_ansi_codes(text)
        padding = width - len(clean_text)
        return border('│') + text + ' ' * padding + border('│')

    # Empty line and divider
    empty_line = create_line(' ' * width)
    horiz_line = create_line(' ' + divider('─' * (width - 2)) + ' ')

    # Build the card with precise spacing
    card = [
        '',
        top_border,
        empty_line,
        create_line(' ' + highlight('Nicholas Bruce') + ' ' + secondary(
            '(') + plain_text('he/him') + secondary(')')),
        horiz_line,
        empty_line,
        create_line(' ' + work('⚙') + '  ' + label('Work') + divider(
            '    ∴ ') + plain_text('Radio telescope engineer @ NRC ') + flag),
        create_line(' ' + bsky('☁') + '  ' + label('Bluesky') +
                    divider(' ∴ ') + handle('@dorktips')),
        create_line(' ' + gh('★') + '  ' + label('GitHub') +
                    divider('  ∴ ') + url('https://github.com/nsbruce')),
        create_line(' ' + email('✉') + '  ' + label('Email') +
                    divider('   ∴ ') + url('nicholas@nicholasbruce.ca')),
        empty_line,
        horiz_line,
        create_line(' ' + divider('>') + ' ' + plain_text('Run') + ' `' + secondary('pipx run') +
                    ' ' + highlight('nicholasbruce') + '` ' + plain_text('anytime to see this card')),
        empty_line,
        bottom_border,
        ''
    ]

    print('\n'.join(card))


if __name__ == "__main__":
    main()
