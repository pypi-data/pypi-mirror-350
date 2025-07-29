from .data import Data
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()
@bindings.add('a')
def _(event):
    " Do something if 'a' has been pressed. "
    print('aaaaa')


def main():
    session = PromptSession()
    v2ex = Data()

    v2ex.run("hot")
    while True:
        try:
            text = session.prompt('> ', auto_suggest=AutoSuggestFromHistory(), placeholder=HTML('<style color="#888888">(please type something)</style>'),)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            v2ex.run(text)

    print('GoodBye!')

if __name__ == '__main__':
    main()
