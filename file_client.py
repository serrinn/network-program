#!/usr/bin/env python3
import socket

HOST, PORT = '127.0.0.1', 9999

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((HOST, PORT))

        # 1) 다운로드 요청
        filename = 'downloaded.bin'
        cli.sendall(f"GET {filename}\n".encode())
        print(f"[Client] Sent request: GET {filename}")

        # 2) 헤더 읽기 (한 줄)
        header = b''
        while not header.endswith(b'\n'):
            chunk = cli.recv(1)
            if not chunk:
                print("[Client] No response from server.")
                return
            header += chunk

        line = header.decode().rstrip('\n')
        # 첫 번째 공백 기준으로 분리: [status, message_or_length]
        status, rest = line.split(' ', 1)

        if status == 'OK':
            # rest에는 파일 길이가 오고, 그만큼 읽어야 함
            length = int(rest)
            print(f"[Client] Server OK, length = {length}")

            # 3) 본문 읽기
            data = b''
            while len(data) < length:
                data += cli.recv(length - len(data))

            # 4) 파일로 저장
            out_name = 'downloaded_' + filename
            with open(out_name, 'wb') as f:
                f.write(data)
            print(f"[Client] Saved {out_name} ({length} bytes)")

        elif status == 'ERROR':
            # rest 전체를 에러 메시지로 출력
            print(f"[Client] Download failed: {rest}")

        else:
            print(f"[Client] Unknown response: {line}")

if __name__ == '__main__':
    main()
