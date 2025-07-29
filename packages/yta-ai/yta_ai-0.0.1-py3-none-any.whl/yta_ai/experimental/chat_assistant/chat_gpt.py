from re_gpt import SyncChatGPT
import requests
import json


def ask_v1(prompt):
    """
    This seems to be working well.
    """
    # You go through this url (https://chat3.aiyunos.top/) and it opens one chat
    # From this chat I made the request: https://715zwv.aitianhu1.top/#/chat/1002
    # You open a new chat, make a request by web, copy cookies and thats all.
    cookies = {
        'sl-session': 'nnQxNXTmBWboDPgV1PA/wg==',
        'sl_jwt_session': 'nBfxJQijBGbhq2HKUw56CQ==',
        'cdn': 'aitianhu',
        'SERVERID': 'srv99n3|ZgSVF',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://715zwv.aitianhu1.top',
        'referer': 'https://715zwv.aitianhu1.top/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    json_data = {
        'prompt': prompt,
        'options': {
            'parentMessageId': 'chatcmpl-97QRFUFrq5WLDuLsTTfUvUPYLaTQK',
        },
        'model': 'gpt-3.5-turbo',
        'OPENAI_API_KEY': 'sk-AItianhuFreeForEveryone',
        'systemMessage': "You are an AI assistant, a large language model trained. Follow the user's instructions carefully. Respond using markdown.",
        'temperature': 0.8,
        'top_p': 1,
    }

    response = requests.post(
        'https://715zwv.aitianhu1.top/api/please-donot-reverse-engineering-me-thank-you',
        cookies = cookies,
        headers = headers,
        json = json_data,
    )
    # The response is a serie of json elements in raw format having the response but
    # in a word-increase way. Each json has a new word. I only care about the last one
    response = response.content
    response = response.splitlines()
    response = json.loads(response[len(response) - 1])

    return response['text']

def ask_v2(prompt):
    """
    ** NOT WORKING **
    This is not working because of a rate limit. I need a 'sign' parameter
    that I don't know where it comes from, and I think that is the one that
    makes the request fail, as I can continue making requests through the
    website. Developed with Astro framework.

    TODO: Keep working to make it work
    """
    # From this: https://chatforai.store/
    import requests
    import datetime

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://chatforai.store',
        'Referer': 'https://chatforai.store/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    # TODO: I don't know where does this sign come from and I need it
    sign = 'b4eb4fd22a63c55c75faedb303507e04c4053d340e99820da157b5ee6f6b2c4b'
    timestamp = str(datetime.datetime.now().timestamp() * 1000)
    data = '{"conversationId":"f317d080-1aaf-414f-88bc-fdee7d4b1c51","conversationType":"chat_single","botId":"chat_single","globalSettings":{"baseUrl":"https://api.openai.com","model":"gpt-3.5-turbo","maxTokens":2048,"messageHistorySize":5,"temperature":0.7,"top_p":1},"prompt":"' + prompt + '","messages":[{"role":"user","content":"' + prompt + '"}],"sign":"' + sign + '","timestamp":' + timestamp + '}'
    data = data.encode()

    response = requests.post('https://chatforai.store/api/handle/provider-openai', headers=headers, data=data)

    print(response)
    print(response.text)
    print(response.content)
    return response.content

def ask_v3(prompt):
    """
    ** NOT WORKING **
    This seems to be working not because of Cloudflare detecting me. I
    don't know how as I can ask through the web page. Maybe is the 
    messages history.
    """
    # From here: https://flowgpt.com/chat
    import requests

    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'authorization': 'Bearer null',
        'content-type': 'application/json',
        'origin': 'https://flowgpt.com',
        'referer': 'https://flowgpt.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-nonce': '',
        'x-signature': '',
        'x-timestamp': '',
    }

    json_data = {
        'model': 'gpt-3.5-turbo',
        'nsfw': False,
        'question': prompt,
        'history': [
            {
                'role': 'assistant',
                'content': 'Hello there 😃, I am ChatGPT. How can I help you today?',
            },
        ],
        'system': "You are help assitant. Follow the user's instructions carefully. Respond using markdown",
        'temperature': 0.7,
        'promptId': 'model-gpt-3.5-turbo',
        'documentIds': [],
        'chatFileDocumentIds': [],
        'generateImage': False,
        'generateAudio': False,
    }

    response = requests.post('https://backend-k8s.flowgpt.com/v2/chat-anonymous', headers=headers, json=json_data)
    # Force it to receive well-written response
    response.encoding = 'utf-8'
    response = response.content
    response = response.splitlines()
    print(response)
    answer_text = ''
    for response_line in response:
        try:
            response_line = json.loads(response_line)
            answer_text += response_line['data']
        except:
            pass

    return answer_text
    #response = json.loads(response[len(response) - 1])

    # Response comes like this 
    """
    {"event":"text","data":"Seg"}

    {"event":"text","data":"ún"}
    """

def ask_v4(prompt):
    """
    This is simple but is working. It seems to be limited to just 25 questions, and 
    is IP-based, so I'm done.
    """
    # From here: https://koala.sh/chat
    cookies = {
        'cf_clearance': 'raYChfDvF_OzTTdMcV19UIIJXxMPE2Y1k1nPH5Fhvn0-1711565095-1.0.1.1-YLtUJHtzM_qv3YVmzFOzN38MXvgiLJEbouvkAd2x3C8WAZ6GKSP6As3PpOOqutPH0GCMGthJojO_5_Xl7iH3bQ',
        '_iidt': 'k7gejbRstP+5a5IOxRdUUQf2RgGTp0vVUDPZDAQxtoTQ45MPQU7NtVDrbuoVlvC+MEJqH0L+pzwZlw==',
        '_vid_t': '0oU1V6DiFStM/i7nXc9Bf8AFH7REsgVV9MjIYwYt9Vcb2RZOcVtUaXgWND9vBu3m1P21fQA6xOT5wg==',
        '__stripe_mid': 'e9642a6d-8941-45a7-a7fa-18d5b155970df1843d',
        '__stripe_sid': 'e42f8f7f-cfee-48d0-83b0-846be8a59508405ab3',
    }

    headers = {
        'accept': 'text/event-stream',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/json',
        'flag-real-time-data': 'false',
        'origin': 'https://koala.sh',
        'referer': 'https://koala.sh/chat',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'visitor-id': 'vMXyv8qXyfcekvaCejnP',
    }

    json_data = {
        'input': prompt,
        'inputHistory': [],
        'outputHistory': [],
        'model': 'gpt-3.5-turbo',
    }

    response = requests.post('https://koala.sh/api/gpt/', headers=headers, json=json_data)
    response
    # Force it to receive well-written response
    response.encoding = 'utf-8'
    response = response.text.split('\n')
    accumulated_text = ''
    for text_line in response:
        if 'data' in text_line:
            accumulated_text += text_line.split(':')[1].strip().replace('"', '')
    return accumulated_text

    # Response is like this below:
    """
            
        data: " de"

        data: " personas"

        data: "."

    """

    # TODO: Continue watching below to get working endpoints:
    # https://github.com/xtekky/gpt4free?tab=readme-ov-file#-providers-and-models
    # https://github.com/zukixa/cool-ai-stuff

def ask_v5(prompt):
    """
    ** NOT WORKING **
    This seems to be working not because of Cloudflare detecting me. I
    don't know how as I can ask through the web page.
    Maybe this (https://stackoverflow.com/a/71404659) or a ChromeDriver instance
    """
    import requests

    headers = {
        'accept': 'application/json',
        'accept-language': 'es',
        'content-type': 'application/json',
        'myshell-client-version': 'v1.5.4',
        'myshell-security-token': 'zfIvFpxwEDNEY1QFABfA+IEGemNJyvDl',
        'myshell-service-name': 'organics-api',
        'origin': 'https://app.myshell.ai',
        'platform': 'web',
        'referer': 'https://app.myshell.ai/',
        'sc-cookie-id': '18e8172f5cd2f5-0d0cc84e196ca68-26001a51-1247616-18e8172f5ce96d',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'timestamp': '1711568924954',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'visitor-id': 'd56026c8-3772-46f2-92fe-840c12cff446',
    }

    json_data = {
        'botId': '4738',
        'message': prompt,
        'messageType': 1,
    }

    response = requests.post('https://api.myshell.ai/v1/bot/chat/send_message', headers=headers, json=json_data)
    response.encoding = 'utf-8'
    response = response.text.split('{')
    print(response)
    response = json.loads('{' + response[len(response) - 1].replace('\n', ''))

    return response['message']['text']

    # Response is like this below:
    """
    
        id: 5131ab92-82ff-44c4-aa8a-89bf52ca4ac9
        event: MESSAGE_REPLY_SSE_ELEMENT_EVENT_NAME_TEXT_STREAM_PUSH_FINISHED
        data: {"content":"", "voiceBytes":"", "voiceBytesIndex":0, "errorReason":"ERROR_REASON_UNSPECIFIED", "status":null, "voiceFilePath":"", "message":null, "audioFileDurationSeconds":0, "userEnergyInfo":null, "imageGenMessageResponse":null}

        id: 34a534ac-9e8f-4e3c-925d-1e2c3ca0e804
        event: MESSAGE_REPLY_SSE_ELEMENT_EVENT_NAME_USER_SENT_MESSAGE_REPLIED
        data: {"content":"", "voiceBytes":"", "voiceBytesIndex":0, "errorReason":"ERROR_REASON_UNSPECIFIED", "status":null, "voiceFilePath":"", "message":{"id":"147195724", "uid":"2965f0771f434eb9a6204b92f263d583", "userId":"8897689", "type":"REPLY", "botId":"4738", "replyUid":"5a26b39eabe0458b8efa74fc282e559e", "status":"DONE", "text":"Según el gobierno metropolitano de Tokio, la población de Tokio en 2021 es de aproximadamente 13,96 millones de habitantes, lo que la convierte en la ciudad más poblada de Japón y una de las más grandes del mundo.", "handled":false, "translation":"", "voiceUrl":"", "voiceFileDurationSeconds":0, "feedbackState":"Normal", "feedbackIssues":[], "createdDateUnix":"1711568926031", "updatedDateUnix":"1711568926031", "audioSpeed":1, "imageGenMessageResponse":null, "embedObjs":[], "imSlashCommandInput":null, "asyncJobInfo":null, "widgetId":"0", "replyId":"147195723", "referenceSource":[], "recommendationQuestion":{"question":[]}, "componentContainer":null, "inputSetting":null}, "audioFileDurationSeconds":0, "userEnergyInfo":null, "imageGenMessageResponse":null}


    """









"""
This below could be working not, sorry
"""

def ask_deprecated(prompt):
    """
    Sends a message through a GPT conversation (using the code-written conversation_id and session
    token). It returns the response.
    """
    # TODO: This is not working, but they are trying to fix it in the 
    # repo (https://github.com/Barrierml/reverse-engineered-chatgpt). 
    # I had to manually re-write 'sync_chatgpt.py' and 'async_chatgpt.py'
    # files but still not working.
    # I receive a 'Cannot concatenate ...' that seems to be something
    # with their code

    # Go to ChatGPT and obtain that Cookie (F12 + Application + Cookies + '__Secure-next-auth.session-token here'
    SESSION_TOKEN = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..uJDTNWyIWEV-Z299.WF6tfBGa1HFc6yU8KyFensoUf8KvnSyzvNk53-pmjD_x3qjiM4ubYzOL-XJhe1yt0RqHJjInig7GG0B1Y6906eCavPOfeevLPmGNlBJGkpBVkiXAhGvnRkQtWNVjzwMYpwF0-U7BzHoVXM0Lv90xm4DDtKnE4FmRWl814mJxToVXdeVGmkjij8yID_RGYE1Ibot5p-gGJQqVG_w6k9v-SopUpZHKaXQbndjj5ORA1rse5E1h_0oU3LPY58dOUud5zIndJ1vE_dsf2kZFYT0hmU_EbjF4qbLcGvpBMFjOaqPLM-FkssIfF4TuZ7svmbKbq53nGmSsFM5O_MGP1EJzY8Uwm3SwN31i8sfFCZhCgGn6Drvkjv0iA8xhGM0aEhqv4r0gAPJpW4bNuabSxpL5X3LGELgk7qSNZ9UFcENmyqv90lLq4SE_CUeQmXajt0JZz8DqmqlYVvIotbRbhq78AC9KS1b0l2Jz8bI-vKmzA7odbp2Juw8BFx4e3386At9lQwjM-vJHTQR1MsQrPse5eHxPak6qLdNHptaQf7XbpxgMEQrSkoki0E-VUtwy7QYtMKffZuL1Vg_SGQk4zrX3dFypH97hqvQ1azZu-dtdLEDO6AtgwUXvcSnmlO3bGUX4zSLFh3oUkAS98AMZgOPYuY4oMk5o8Q6P700hJhfzQgvek59OX__snqeTO3Sltc8R14N84UWqFYFcl0X6wonB09m4zZvgzy8qBNGgeoxAUF6LrV8RD2yAYvDytrqcP6QuIbNN6RvqgDVN3EYT3lGLLBa3higJKA_l6DWin3uB984_icNQ9p93P4BI61BW_uL8FHMcj1pZ4pyPA3gVmTINY1gfwc8-ObPgQW67VnL57shi3BD5ujdU6_gqNL53sw-96HwBnJXJKLwaxwF5t_I7fyTcKq-fx-qaYiYVpLrDL3g3JylZ-jElQDLN5gN_GJ0MkGo8gUC_T0XK6w4MoOdU60zVCWEFoJ10Q-qIEfNr3F-URlh-LnLt0SS2uDdjMvLdEbXj3A_lVjFVHoQmujSMs_E0GcAgSUb6zBvnzZO7yvUYwfyqGvJwbaCDxa9bq7Ec2bb1MKn3bqOJJvHRSBbzGYVVXshT4WUOlqh24hBP9hgaT4BwooGI9jhRw_rda0rAZ6IlvBazZQ33qZzVbc5W3nyxNUIzbhUICX96pTlCSPZcRlmtItxsCljLxrzHTsij6QQxtJ0ugr8IvFzTisaST5qQgZwLtgPSf7Y2NRkkY_16etKhEuAwFWLbm374xp475Wyj5RNNPF8BzS-N38JSjrH5iu8yvTEaB_VHYgVsUYiuHY-R4zkVyIAsULemqB6pki3PPIQzJkAY99INI72ZRcWdyZycs-jxUrVuZh35CJpYr9WbgTpwrpW9Kz6K6qnFWblsv507dz4sr5uWskXr-xqavvTPVQh2-_9idRmSa1YweMt9FVzNLLg_aJqMtYXqJf5z_iFcliVfTConsHWL0fpHjJyIyKZOje4m-SEk_2FlkdbRr2FqkTequNxS1ND2rj5wroR1p9BVybwRDiKNYrAQuGnZHltQicJzYPjFphCzdPKMfQGJRtAYCkNM-Nq-V3k3iZ4vF37H1PP-swxnp-neus2K_YuH6KeVOTKMK74F3HMJJLkuBmMn4D15iBcd4K8PBvaeVxZi9tsfFX0TElE2gJzwjLAc2kJQxZzwn-SwK5BSsKPLMMjoAO3XBnD2VwlplXV5nk92PSSFhl4-T8WetMEOn5QkJBOH36cbxSbCYgDOB90AbfhdpvAVgiX1mcqBSHp51ISbvXrerGWNkMrP20E0V_FHG5MCqwH1YvV2FKPo8PFC3gv96q60HrffwF96gu0v5OtqGtHR2k3aevwuNUqB4smXF04fd6tRJLyHq1fYu5PvyXYQrzSp27UVtuHAfxXb38KLw-Gdn95R1P_LBps9OTU71BPkYZwbAA69UaPk4R5rkX832tGHMTM5HOE8ChSQk-pfaPzuE6UpXJ0nh4EncyKQCYl57oY0B1JSc_-WEmOlYhM6F5Cata_lkuC_JUlAaEsgGNosfW1qhksbSgSlQMQEmLCHP7p-eA4-UQnkgb1OR2sxdW7qCnXKICKiEftanAgYZbB6ha2c9xsHMVClkk-2Nui5XhSVx5Bo-QlZnjp0p5c7Xw-JDLY1uwmmoXYCaCKpLMJZkXpg_q8p-H5gR-jAoPoCsw3ajLGrkm36ubbKPc9_Nn3KQzXHg9GWxf35OeSu6CVvJAy7WGvtnlwnLnBlURMt9nRSgn341UN-jsyWrdnQQLu0ygwMDQMaJF-_M_8HxfmerssdT810Z3MGuhX14_2CMQ8pTI8fj_GUwe47NIj9OOpX697F-kzUMk_Q6SPCmJjPoPCoC2e4Z_f1ef8macrFJW5q_qMcBsOauDl5pPZvjkXCi-dlBBacAvdTKzO45dXPD7bxkOVJnok9kITp2VgVz5kr6HYLhsq98aM1SM_CZSdKDJaatokSZPP_JSYIOfnZdnqnnzIWQJXjZTTnTIFoGGR_AR8tokVptlpUszJUHnAtltdNi5B6mdsleeg4LJzpToHwMzd0iAn2TOsXgAwtdIcib7K9ppEk5mvj9oF3QAPkegEB83skfUAQGQSEBgtRXG6jjEm6on8WuaYRU8nrkSCiIQ2Opv-cWaaSfVDAm4t_Zz6ln59rBmLcVPpyi9CYsNhoGyReClj6hnrRhK6hciwnrVOMtoQ9T1LyfdGsBE4ZEX_AqDMfqO_pz58yvFFzMduRPVO-y8g2YVMNkH_R9R_qRXCHtTlJPcn2TOi9wuDf-ZK1WDLXBVV02wI2NOloVFGYTLvhJqnG6mEv3YkdGbIAsREWxUF01g.YcvVAzSNW20DDyUDL313Jw"
    CONVERSATION_ID = "31ca0c4a-77a0-4f1a-9161-9fd38dfe1afd"
    
    with SyncChatGPT(session_token = SESSION_TOKEN) as chatgpt:
        if CONVERSATION_ID:
            conversation = chatgpt.get_conversation(CONVERSATION_ID)
        else:
            # TODO: This below is untested, so I would store that new conversation_id I think
            conversation = chatgpt.create_new_conversation()

        response = ""

        for message in conversation.chat(prompt):
            response += message['content']

        return response
    
def get_image_generation_prompt(idea):
    """
    Returns the GPT response about a nice midjourney prompt to represent the provided 'idea'.
    """
    return __ask_gpt(__get_image_generation_prompt_input(idea))

def get_stock_video_keywords(idea):
    """
    Returns the GPT response about nice stock video keywords to look for the perfect video that
    fits the provided 'idea'.
    """
    return __ask_gpt(__get_stock_video_input(idea))

def get_feeling_from_input(input):
    """
    Returns the GPT response about the feeling that the provided 'input' transmits.
    """
    return __ask_gpt(__get_feeling_from_input(input))

def get_topic_from_input(input):
    """
    Returns the GPT response about the main topic of the provided 'input' talks about.
    """
    return __ask_gpt(__get_topic_from_input(input))

def get_translation(input, input_language = 'inglés', output_language = 'español'):
    """
    Returns the provided 'input' English text translated into Spanish.
    """
    return __ask_gpt(__get_translate_text_input(input, input_language, output_language))

def test(input):
    """
    This method is for testing. Asks GPT the 'input' and returns its response.
    """
    return __ask_gpt(input)

"""
    ¿Habla de personas o de cosas?
    '¿Me puedes decir si la frase "esto es una casa, no hay más que verlo" está hablando sobre personas o sobre cosas? Solamente respóndeme "personas" si está hablando de personas, o "cosas" si está hablando de cosas.')

    ¿Tema de la frase?
"""