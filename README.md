# Boolean Interpreter
Project for Concepts of Programming languages.
Consists of a Lexical analyzer and an interpeter for boolean expressions.

Information on what a Grammer is can be found [here](https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Grammars)

## Language
```
<B>       := <IT>.
<IT>      := -> <OT><IT_Tail>
          :=
<IT_Tail> := -> <OT><IT_Tail>
          :=
<OT>      := <AT> <OT_TAIL>
<OT_Tail> := v<AT> <OT_Tail>
          :=
<AT>      := <L><AT_Tail>
<AT_Tail> := ^ <L> <AT_Tail>
          :=
<L>       := <A>
          := ~<L>
<A>       := T
          := F
          := (<IT>)
```
  
## Syntax:
Valid Tokens:
- `.` (EOF)
- ` ` (whitespace)
- `^` (and)
- `v` (or)
- `->` (implies)
- `~` (not)
- `T` (true)
- `F` (false)
- `(` (left parenthesis)
- `)` (right parenthesis)
- error otherwise

## Examples:
| Expression    | Evaluation    |
| ------------- |:-------------:|
| `T.`    | true |
| `T v F.`      | true      |
| `T -> T.` | true      |
| `~T.` | false |
| `T -> (T -> (F -> ~T)).` | true |

Any syntactically incorrect expressions will result in an error message and a prompt for another expression.
