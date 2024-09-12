import requests
NEURONET_API = "key-3UmyrxjLLFvZ2bu6TTPFnmXQd9rEqRTwPaxez6sME2UzaHOFX76XuyVFPnkim8M52qmFckkXqvK8xa5mlAX0vMzqna6M0M0V"
TOKEN_BOT = '7327702608:AAFkDZ-ZBTNvJ1uW2Fglm5bORc_Fhiz359o'
PAYMASTER_TOKEN = '1744374395:TEST:29858c9d68df9e2eaffb'

def zapros(prompt, style):
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer key-3UmyrxjLLFvZ2bu6TTPFnmXQd9rEqRTwPaxez6sME2UzaHOFX76XuyVFPnkim8M52qmFckkXqvK8xa5mlAX0vMzqna6M0M0V',
        'content-type': 'application/json',
    }

    json_data = {
        'style': f'{style}',
        'prompt': f'{prompt}',
        'output_format': 'jpeg',
        'response_format': 'url',
        "negative_prompt_2": 'Baby, Kid, Child, verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.8),cross-eyed,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, extra long fingers, armpit hair, hair on legs, legs and arms from the vagina, two heads, merging of bodies, bad hands, bad vagina anatomy, merging of legs, merging stops, text, error, missing fingers, extra digit, more than 5 fingers, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, three legs, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, big vagina, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, ((repeating hair))'
    }
    response = requests.post('https://api.getimg.ai/v1/essential-v2/text-to-image', headers=headers,
                                 json=json_data).json()

    return list(response.values())[-1]
