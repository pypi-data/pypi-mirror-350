# I found this (https://github.com/f/awesome-chatgpt-prompts) that could help

def get_image_generation_input_prompt(idea):
    """
    Returns the input prompt to ask GPT for a prompt that would use in midjourney to generate
    an incredible AI image based  on the provided 'idea'.
    
    Explicitly requests that only the prompt be responded to, without any additions.
    """
    return "¿Cuál sería el prompt que utilizarías para que MidJourney te crease una imagen que represente la idea '" + idea + "'? Respóndeme única y exclusivamente con el prompt, sé conciso."

def get_stock_video_input_prompt(idea):
    """
    Returns the input prompt to ask GPT for a key phrase that would use in YouTube to search
    for the perfect video to fit the provided 'idea'.

    Explicitly requests that only the key phrase be responded to, without any additions.
    """
    #return "quiero que me seas conciso y no me digas nada más que no sea qué palabras clave utilizarías para buscar un vídeo en Youtube que pueda servir para poner de fondo en un vídeo y que represente la frase '" + idea + "'"

    return "¿Cuál sería una frase que podrías usar para buscar en YouTube un vídeo de stock que pueda poner de fondo en otro vídeo mientras hablo de " + idea + " y que en dicho vídeo se represente eso de lo que estoy hablando, como si fuera un vídeo de stock? Respóndeme única y exclusivamente con la frase, sé conciso."

def get_feeling_from_input_prompt(input):
    """
    Returns the input prompt to ask GPT for the feeling that the provided 'input' (that 
    is a text) that conveys.

    Explicitly requests that only the feeling be responded to, without any additions.
    """
    return "Me han dicho la frase " + input + " y necesito saber qué tipo de sentimiento transmite esa frase. Solo quiero que me respondas el sentimiento, única y exclusivamente, así que sé concisco. No me des más de una opción. Dame solo una opción."

def get_topic_from_input_prompt(input):
    """
    Returns the input prompt to ask GPT for the main topic that is being talked about in
    the provided 'input'.

    Explicitly requests that only the topic be responded to, without any additions.
    """
    return "¿Me puedes cuál es el tema principal del que se habla en la frase '" + input + "'? Solamente respóndeme con el tema, sé conciso. No me des más de una opción. Dame solo una opción."

def get_translate_text_input_prompt(input, input_language = 'inglés', output_language = 'español'):
    """
    Returns the input prompt to ask GPT for a translation from 'input_language' to 'output_language'
    of the provided 'input'.

    Explictly requests that only the translation be responded to, without any additions.
    """
    return "¿Puedes traducirme el texto que te voy a pasar a continuación del " + input_language + " al " + output_language + "? Solo quiero que me respondas con el texto traducido, sé conciso. No añadas nada más que el texto. El texto es el siguiente, que te lo mando entrecomillado. '" + input + "'"

def get_script_prompt(input, num_of_chars):
    return 'Quiero que actúes como si fueras un escritor profesional muy bueno de guiones de vídeos de Youtube. Sabes generar guiones que mantienen la atención del espectador durante todo el tiempo, y el guion es tan espectacular que lo querrían las principales empresas de Hollywood de lo bueno que es. Te voy a dar la idea sobre la que tratará el guion y tú me respondes única y exclusivamente con ese guión. El guion debe contar con un total de ' + str(num_of_chars) + ' caracteres, y la idea es "' + input + '".'

def get_youtube_summary_from_subtitles_prompt(input):
    #return 'Tengo los subtítulos de un vídeo de Youtube. ¿Me puedes hacer un resumen de lo que pasa en el vídeo? Quiero que el resumen sea por capítulos. No quiero que me digas nada más que el resumen en sí, pero que este sea bastante detallado en cada capítulo. Estos son los subtítulos: "' + input + '"'

    #return 'Te voy a dar los subtítulos de un vídeo de Youtube. Quiero que me hagas un resumen de unos mil caracteres de largo, todo en un mismo párrafo, sin saltos de línea, como si fuese una historia. Estos son los subtítulos: "' + input + '"'

    return 'Tengo los subtítulos de un vídeo. Quiero que me expliques lo que pasa en el vídeo, sin saltos de línea ni títulos ni nada, en un solo párrafo, como si fuese una historia. No seas escueto. Estos son los subtítulos: "' + input + '"'

    # This one returns me line breaks, asterisks, titles... It works for a human, but not for me
    #return 'Quiero que actúes como si fueras alguien que se dedica a crear vídeos en Youtube. Eres experto en crear guiones, a modo de historia, para vídeos de Youtube. Te voy a dar los subtítulos de un vídeo y quiero que me reconstruyas un guion que sirva para narrar otro vídeo nuevo sobre lo que se habla en el vídeo del que te paso los subtítulos a continuación. Solamente quiero que me des como respuesta el guion, sin títulos, sin líneas de separación. Todo seguido en el mismo párrafo, aunque sea muy muy largo. No quiero saltos de línea ni títulos, todo seguido, en la misma línea. Los subtítulos son los siguientes: "' + input + '"'

def get_story(input):
    """
    Returns a story from a professional storyteller that talks about the provided 'input' idea.
    It comes in different paragraphs, so it could be a good idea to use each one as a segment.
    """
    return 'Quiero que actúes como si fueras un narrador de historias, un storyteller. Vas a ser capaz de inventar increíbles historias que tienen gancho, que son imaginativas y que mantienen la atención de la audiencia hasta el final. Pueden ser historias educacionales, inventadas, basadas en hechos reales o cualquier tipo de historias que tengan el potencial de capturar la atención e imaginación de la gente. Dependiendo del tipo de audiencia, vas a elegir diferentes temas para tu historia. Por ejemplo, si son niños puedes hablar sobre animales. Si son adultos, puedes hablar sobre historias basadas en hechos reales que cautiven mejor a esa audiencia. Mi primera petición es: "' + input + '"'

def get_english_song(topic, chars_length):
    return 'Quiero que actúes como si fueses un increíble compositor de canciones en inglés y que me des la letra de una canción. Quiero que la canción tenga máximo ' + str(chars_length) + ' caracteres, que trate sobre ' + topic + ', y que esté en inglés. Respóndeme solo con la letra de la canción directamente.'