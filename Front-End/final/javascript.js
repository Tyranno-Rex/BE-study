const sliderWrap = document.querySelector(".slider__wrap");
const sliderImg = document.querySelector(".slider__img");       // 보여지는 영역
const sliderInner = document.querySelector(".slider__inner");   // 움직이는 영역
const slider = document.querySelectorAll(".slider");            // 이미지
const sliderDot = document.querySelector(".slider__dot");       //닷 메뉴

// 이미지 갯수에 따라 닷메뉴 생성되도록 만들어야함

let currentIndex = 0;                       // 현재 이미지
let sliderCount = slider.length;            // 이미지 갯수
let sliderWidth = sliderImg.offsetWidth;    // 이미지 가로값
let dotIndex = "";

// 초기값 설정 함수 init()
function init(){
    // <a href="#" class="dot active">이미지1</a>
    slider.forEach(() => {dotIndex += "<a href='#' class='dot'>이미지1</a>";});
    sliderDot.innerHTML = dotIndex;
    // 첫 번째 닷 버튼에 활성화 표시(active)
    sliderDot.firstChild.classList.add("active");
}
init();

// 이미지 이동
function gotoSlider(num){
    sliderInner.style.transition = "all 500ms";
    sliderInner.style.transform = "translateX("+ -sliderWidth * num +"px)";
    currentIndex = num;

    // 두번째 이미지 == 두번째 닷에 클래스 추가
    // 닷 메뉴 클래스 모두 삭제 -> 해당 이미지의 닷 메뉴에 클래스 추가
    let dotActive = document.querySelectorAll(".slider__dot .dot");
    dotActive.forEach(el => el.classList.remove("active"));
    dotActive[num].classList.add("active");
}

// 버튼 클릭했을 때
document.querySelectorAll(".slider__btn a").forEach((btn, index) => {
    btn.addEventListener("click", () => {
        let prevIndex = (currentIndex + (sliderCount -1)) % sliderCount;
        let nextIndex = (currentIndex + 1) % sliderCount;

        if(btn.classList.contains("prev")){
            gotoSlider(prevIndex);
        } else {
            gotoSlider(nextIndex);
        }
    });
})

// 닷 버튼을 클릭했을 때 해당 이미지로 이동
document.querySelectorAll(".slider__dot .dot").forEach((dot, index) => {
    dot.addEventListener("click", () => {
        gotoSlider(index);
    });
})