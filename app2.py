from flask import Flask, request, render_template  # Importar las clases y funciones necesarias de Flask
import ply.lex as lex  # Importar el módulo lex de PLY para el análisis léxico
import ply.yacc as yacc  # Importar el módulo yacc de PLY para el análisis sintáctico

# Inicializa la aplicación Flask
app = Flask(__name__)

# Definir palabras reservadas que serán reconocidas por el analizador léxico
reserved = {
    'for': 'PALABRA_RESERVADA',  # Palabras reservadas
    'while': 'PALABRA_RESERVADA',
    'if': 'PALABRA_RESERVADA',
    'else': 'PALABRA_RESERVADA',
    'class': 'PALABRA_RESERVADA',
}

# Definir la lista de tokens que el analizador léxico reconocerá
tokens = [
    'PALABRA_RESERVADA',
    'IDENTIFICADOR',
] + list(set(reserved.values()))  # Añadir todas las palabras reservadas a la lista de tokens

# Expresión regular para reconocer las palabras reservadas
def t_PALABRA_RESERVADA(t):
    r'\b(for|while|if|else|class)\b'  # Expresión regular para identificar las palabras reservadas
    t.type = reserved.get(t.value, 'PALABRA_RESERVADA')  # Asignar el tipo correcto basado en las palabras reservadas
    return t

# Expresión regular para identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Expresión regular para identificar identificadores
    t.type = 'IDENTIFICADOR'  # Asignar el tipo 'IDENTIFICADOR'
    return t

# Regla para contar las líneas nuevas en el texto de entrada
def t_newline(t):
    r'\n+'  # Expresión regular para identificar saltos de línea
    t.lexer.lineno += len(t.value)  # Incrementar el número de línea del lexer

# Manejo de errores léxicos (cuando un token no es reconocido)
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")  # Imprimir un mensaje de error para el carácter no reconocido
    t.lexer.skip(1)  # Ignorar el carácter ilegal

# Construir el lexer utilizando las reglas definidas
lexer = lex.lex()

# Función que realiza el análisis léxico sobre el texto ingresado
def lexer_analysis(text):
    lexer.input(text)  # Configurar el texto de entrada para el lexer
    tokens = []
    for tok in lexer:
        # Convertir el tipo a un formato más amigable
        if tok.type == 'PALABRA_RESERVADA':
            token_type = 'PALABRA RESERVADA'  # Convertir el tipo a 'PALABRA RESERVADA'
        else:
            token_type = tok.type
        tokens.append({
            'line': tok.lineno,  # Número de línea del token
            'column': tok.lexpos,  # Posición del token en la línea
            'value': tok.value,  # Valor del token
            'type': token_type  # Tipo del token
        })
    return tokens

# Definir la regla sintáctica para la estructura 'for'
def p_statement_for(p):
    'statement : PALABRA_RESERVADA'  # Regla para identificar una declaración de palabra reservada
    p[0] = {'line': 1, 'type': 'FOR', 'correct': True, 'incorrect': False}  # Establecer la estructura correcta

# Regla para manejar errores sintácticos
def p_statement_error(p):
    '''statement : error'''  # Regla para manejar errores en la sintaxis
    p[0] = {'line': 1, 'type': 'ERROR', 'correct': False, 'incorrect': True}  # Establecer la estructura incorrecta

# Función para manejar errores en el análisis sintáctico
def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")  # Imprimir un mensaje de error para el error de sintaxis

# Construir el parser usando las reglas definidas
parser = yacc.yacc()

# Función que realiza el análisis sintáctico sobre el texto ingresado
def syntax_analysis(text):
    syntax_structures = []
    tokens = text.split()  # Dividir el texto en tokens
    for token in tokens:
        if token == "for":
            syntax_structures.append({'line': 1, 'type': 'for', 'correct': True, 'incorrect': False})  # Estructura correcta
        else:
            syntax_structures.append({'line': 1, 'type': token, 'correct': False, 'incorrect': True})  # Estructura incorrecta
    return syntax_structures

# Definir la ruta principal de la aplicación Flask
@app.route('/', methods=['GET', 'POST'])
def index():
    text = None
    lex_tokens = []
    syntax_structures = []
    error_message = None

    if request.method == 'POST':  # Si el método de solicitud es POST
        text = request.form['text']  # Obtener el texto del formulario
        if text:
            try:
                lex_tokens = lexer_analysis(text)  # Realizar el análisis léxico
                syntax_structures = syntax_analysis(text)  # Realizar el análisis sintáctico
            except Exception as e:
                error_message = f"Error en el análisis: {str(e)}"  # Manejar excepciones durante el análisis

    return render_template('index2.html',  # Renderizar la plantilla HTML
                           text=text,
                           lex_tokens=lex_tokens,
                           syntax_structures=syntax_structures,
                           error_message=error_message)

# Ejecutar la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)