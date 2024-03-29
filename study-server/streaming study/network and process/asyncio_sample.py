import asyncio
import time

# asnyc 함수를 사용하면 함수를 비동기로 사용할 수 있다.
# 이러한 async 함수를 사용하면 여러개의 함수를 동시에 실행할 수 있다.
# 비동기 함수를 코루틴이라고 부른다.
async def sleep():
    await asyncio.sleep(1) # 해당 방식 대신 time.sleep()을 사용하면 동기 방식으로 실행 시간을 줄일 수 없다.
    
# 또한 코루틴 안에서 다른 코루틴을 호출할 때 await sleep()와 같이 await를 사용해야 한다.
# await로 호출한 코루틴이 종료될 때 까지 기다리지 않고 제어권을 메인 스레드나 다른 코루틴에게 넘겨준다.
# 이러한 방식이 비동기 방식 = non-blocking 방식이다.
    
async def sum(name, numbers):
    start = time.time()
    total = 0
    for number in numbers:
        await sleep()
        total += number
        print(f'작업중={name}, number={number}, total={total}')
    end = time.time()
    print(f'작업명={name}, 걸린시간={end-start}')
    return total

async def main():
    start = time.time()

    # 해당 코드는 수행한 코루틴 작업을 생성한다. 
    # 여기서는 작업이 생성할 뿐이지 코루틴이 실행되지는 않는다.
    task1 = asyncio.create_task(sum("A", [1, 2]))
    task2 = asyncio.create_task(sum("B", [1, 2, 3]))
    
    
    # 해당 코드는 실질적인 코루틴의 실행을 담당한다.
    await task1
    await task2

    
    result1 = task1.result()
    result2 = task2.result()
    end = time.time()
    print(f'총합={result1+result2}, 총시간={end-start}')

if __name__ == "__main__":
    asyncio.run(main())
