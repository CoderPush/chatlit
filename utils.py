
def link_button(st, text, path):
    st.write(
        f'''
        <a target="_self" href="{path}">
            <button kind="secondary" class="css-w770g5 edgvbvh10">
                <div class="css-x78sv8 e16nr0p34">
                {text}
                </div>
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )
