import streamlit as st

from index import get_autocomplete_suggestions

def main():
    st.title("Auto Complete")
    
    
    # Exibindo o texto inserido pelo usuário
    texto = st.text_input("Digite um termo:")
    if texto:
        suggestions = get_autocomplete_suggestions(texto)
        st.write(f"Resultado da busca pelo termo: '{texto}': ")
        for suggestion in suggestions:
            st.write(suggestion)
            

if __name__ == "__main__":
    main()
