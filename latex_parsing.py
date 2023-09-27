# third-party
import re

# local 
from string_aux_functions import try_search

def parse_text_formatting(test_string):

    test_string = test_string.replace('\\textbackslash ', '\\')

    url_items = re.findall(r'\\url{([^}]*)}', test_string)
    for url_item in url_items:
        test_string = test_string.replace(f'\\url{{{url_item}}}', f'[{url_item}]({url_item})')

    bold_items = re.findall(r'\\textbf{([^}]*)}', test_string)
    for bold_item in bold_items:
        test_string = test_string.replace(f'\\textbf{{{bold_item}}}', f'**{bold_item}**')

    italic_items = re.findall(r'\\textit{([^}]*)}', test_string)
    for italic_item in italic_items:
        test_string = test_string.replace(f'\\textit{{{italic_item}}}', f'*{italic_item}*')

    texttt_items = re.findall(r'\\texttt{([^}]*)}', test_string)
    for texttt_item in texttt_items:
        test_string = test_string.replace(f'\\texttt{{{texttt_item}}}', f'`{texttt_item}`')

    ref_items = re.findall(r'\\ref{([^}]*)}', test_string)
    for ref_item in ref_items:
        test_string = test_string.replace(f'\\ref{{{ref_item}}}', f'`{ref_item}`')

    test_string = test_string.replace('\\_', '_')
    test_string = test_string.replace('\\newpage', '')

    return test_string

def parse_enumerate(test_string): # TODO: substitutes by itemize
    '''
     Returns
     -------
     test_string: str
        Original string with itemize format removed
     '''

    test_string = test_string.replace('\\begin{enumerate}', '')
    test_string = test_string.replace('\\end{enumerate}', '')
    test_string = test_string.replace('\\item', '- ')

    return test_string


def parse_itemize(test_string):
    '''
    Returns
    -------
    test_string: str
    Original string with itemize format removed
    '''
    
    test_string = test_string.replace('\\begin{itemize}', '')
    test_string = test_string.replace('\\end{itemize}', '')
    test_string = test_string.replace('\\item', '- ')

    return test_string

def parse_sections(test_string):

    section_titles = re.findall(r'\\section{([^}]*)}', test_string)
    for i,title in enumerate(section_titles):
        test_string = test_string.replace(f'\\section{{{title}}}', f'# <span style="color:#00aba1;"> {i+1}. {title.strip()} </span>')


    subsection_titles = re.findall(r'\\subsection{([^}]*)}', test_string)
    for i,title in enumerate(subsection_titles):
        test_string = test_string.replace(f'\\subsection{{{title}}}', f'## <span style="color:#484848;"> {title.strip()}  </span>')

    
    subsubsection_titles = re.findall(r'\\subsubsection\*{([^}]*)}', test_string)
    for i,title in enumerate(subsubsection_titles):
        test_string = test_string.replace(f'\\subsubsection*{{{title}}}', f'##### <div style="color:#484848"> {title.strip()} </div>')

    return test_string



def parse_code(test_string):

    test_string = test_string.replace('\\begin{lstlisting}[language=Python]', '```(python)')
    test_string = test_string.replace('\\begin{lstlisting}[language=C++]', '```')
    test_string = test_string.replace('\\end{lstlisting}', '```')

    # code_items = re.findall(r'\\begin{lstlisting}\[language=Python]([^\\?!]*)\\end{lstlisting}', test_string)
    # for code_item in code_items:
    #     test_string = test_string.replace(f'\\begin{{lstlisting}}[language=Python]{code_item}\\end{{lstlisting}}', f'```(python)\n{code_item}\n```')
    
    # code_items = re.findall(r'\\begin{lstlisting}\[language=C\+\+\]([^\\?!]*)\\end{lstlisting}', test_string)

    # for code_item in code_items:
    #     test_string = test_string.replace(f'\\begin{{lstlisting}}[language=C++]{code_item}\\end{{lstlisting}}', f'```\n{code_item}\n```')

    
    
    return test_string


def parse_figures(test_string):

    figure_items = re.findall(r'\\begin\{figure\}[^}]*\\includegraphics\[width=([^}]*)\\linewidth\]\{([^}]*)}[^}]*\\caption\{([^}]*)}', test_string)
    non_figure_items = re.split(r'\\begin\{figure\}[^}]*\\includegraphics\[width=[^}]*\\linewidth\]\{[^}]*\}[^}]*\\caption\{[^}]*\}[^}]*\\label\{[^}]*\}[^}]*\\end{figure}', test_string)

    new_test_string = ''

    for i, figure in enumerate(figure_items):
        size = figure[0]
        figure_path = figure[1]
        caption = figure[2]

        new_test_string += non_figure_items[i]
        new_test_string += f'<img src="{figure_path}" width="450" style="display=block; margin:auto"/> <p style="color:#484848;text-align:center"> <i> Figure {i+1}: {caption} </i> </p>'
    
    new_test_string += non_figure_items[-1]

    figure_items = re.findall(r'\\begin\{figure\}[^}]*\\begin\{minipage\}\{([^}]*)\\linewidth\}[^}]*\\includegraphics\[width=[^}]*\\linewidth\]\{([^}]*)}[^}]*\}\%[^}]*\}[^}]*\\begin\{minipage\}\{([^}]*)\\linewidth\}[^}]*\\includegraphics\[width=[^}]*\\linewidth\]\{([^}]*)}[^}]*\}[^}]*\\caption\{([^}]*)\}[^}]*\\label\{[^}]*\}[^}]*\\end{figure}', new_test_string)
    non_figure_items = re.split(r'\\begin\{figure\}[^}]*\\begin\{minipage\}\{[^}]*\}[^}]*\\includegraphics\[width=[^}]*\\linewidth\]\{[^}]*}[^}]*\}\%[^}]*\}[^}]*\\begin\{minipage\}\{[^}]*\}[^}]*\\includegraphics\[width=[^}]*\\linewidth\]\{[^}]*}[^}]*\}[^}]*\\caption\{[^}]*\}[^}]*\\label\{[^}]*\}[^}]*\\end{figure}', new_test_string)

    new_test_string = ''
    
    for i, figure in enumerate(figure_items):
        size1 = figure[0]
        figure_path1 = figure[1]
        size2 = figure[2]
        figure_path2 = figure[3]
        caption = figure[4]

        new_test_string += non_figure_items[i]
        new_test_string += f'<table><tr>\n<td> <img src="{figure_path1}" width="350"/>  </td>\n<td> <img src="{figure_path2}" width="350"/>  </td>\n</tr></table>\n<p style="color:#484848;text-align:center"> <i> Figure {i+1}: {caption} </i> </p>'
    
    new_test_string += non_figure_items[-1]
    
    return new_test_string



def parse_quotes(test_string):
    '''
    Returns
    -------
    test_string: str
    Original string with quote format removed
    '''

    test_string = test_string.replace('\emojiflash', '⚡')
    test_string = test_string.replace('\emojiwarning', '⚠️')
    test_string = test_string.replace('\emojiwrite', '✏️')

    quotes = re.findall(r'\\begin{quote}(\n*[^}]*)\\end{quote}', test_string)
    for quote in quotes:
        new_quote = quote.replace('\n', '\n> ')
        test_string = test_string.replace(f'\\begin{{quote}}{quote}\\end{{quote}}', f'{new_quote}')

    return test_string


def remove_comments(test_string):

    return re.sub(r'^%.*\n?', '', test_string, flags=re.MULTILINE)