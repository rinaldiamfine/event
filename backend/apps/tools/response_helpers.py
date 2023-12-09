

def response_mapper(status, datas, title, message):
    if (status == True):
        return {
            "title": title,
            "message": message,
            "datas": datas
        }
