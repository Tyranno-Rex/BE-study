import folium

def show_map_with_number(latitude, longitude, number):
    # Folium을 사용하여 지도 객체 생성
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # 지정된 위치에 마커 추가
    folium.Marker([latitude, longitude], 
                    popup=f'Number: {number}',  # 숫자를 팝업에 표시
                    icon=folium.DivIcon(html=f'<div style="font-size: 16pt;">{number}</div>')
                    ).add_to(m)
    
    # 생성한 지도를 HTML 파일로 저장하여 브라우저에서 열기
    m.save('./tasu/map/map_db/first_map.html')

# 특정 위도와 경도, 표시할 숫자를 입력
latitude = 37.5665  # 예시 위도
longitude = 126.9780  # 예시 경도
number = 10  # 표시할 숫자

# 함수 호출하여 지도에 숫자 표시
show_map_with_number(latitude, longitude, number)
