from streamlit_marquee import streamlit_marquee


def marquee():
    streamlit_marquee(**{
        # the marquee container background color
        'background': "#000000",
        # the marquee text size
        'font-size': '12px',
        # the marquee text color
        "color": "#ffffff",
        # the marquee text content
        'content': 'Stay turn. More features are developing now. '*3,
        # the marquee container width
        'width': '1920px',
        # the marquee container line height
        'lineHeight': "10px",
        # the marquee duration
        'animationDuration': '15s',
    })
