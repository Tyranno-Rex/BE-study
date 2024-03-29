"""
ssl(secure socket layer)은 네트워크 통신을 보안하는 프로토콜이다.
공개키 암호와 방식을 사용하여 데이터를 암호화하고 복호화한다.


ssl을 사용하면 소켓 서버/클라이언트간에 간단하게 공개키 방식의 암호화를 적용할 수 있다.

CA.key: 공개키
CA.pem: 공개키로 만든 인증서 (클라이언트에게 제공해야하는 인증서)
server.key: 비밀키(서버에만 있는 비밀키)
server.crt: 비밀키로 만든 인증서(서버에만 있어야하는 인증서)


인증서 생성하기
1. openssl genrsa -out CA.key 2048

"""