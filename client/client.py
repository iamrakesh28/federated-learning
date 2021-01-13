from sender import Sender

def main():
    send_obj = Sender('http://127.0.0.1:5000')
    data = {'id' : 2}
    send_obj.send(data=data, request='post')
    print(send_obj.get_resp_text())
    print(send_obj.get_resp_status())

if __name__ == "__main__":
    main()
