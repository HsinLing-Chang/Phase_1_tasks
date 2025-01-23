let url =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
// 設定 navbar選單按鈕
const toggleBtn = document.querySelector(".toggle-btn");
const navBar = document.querySelector(".nav-bar");

toggleBtn.addEventListener("click", () => {
  navBar.classList.toggle("active");
  toggleBtn.classList.toggle("active");
});
// 設定loadmore
let currentValue = 0;
const loadMoreBtn = document.querySelector(".load-more");
loadMoreBtn.addEventListener("click", () => {
  let times;
  if (currentValue + 10 > 58) {
    times = 58 - currentValue;
  } else {
    times = 10;
  }
  addNewDiv(times);
  renderPage(currentValue, times);
  // console.log(`currentValue: ${currentValue}`);
});

// 抓取url內容並return spotTitleAndImg
async function fetchData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    const spotInfo = data.data.results;
    // console.log(spotInfo);
    const spotTitleAndImg = []; //[{Title: "新北投溫泉區",image: img_url}]
    for (const info of spotInfo) {
      let imgLink = info.filelist.split("https://")[1];
      imgLink = "https://" + imgLink;
      // for (const i in imgLink) {
      //   imgLink[i] = "https://" + imgLink[i];
      // }
      const spot = {
        Title: info.stitle,
        image: imgLink,
      };
      spotTitleAndImg.push(spot);
    }
    // console.log(spotTitleAndImg);
    return spotTitleAndImg;
  } catch (e) {
    console.log(e);
  }
}
//創建新Container
function addNewDiv(num) {
  const container = document.querySelector(".container");
  // console.log(container);
  for (let i = 0; i < num; i++) {
    const imgContainer = document.createElement("div");
    imgContainer.classList.add("item", "box", "img", "img-container");
    const starImg = document.createElement("img");
    starImg.classList.add("star");
    starImg.src = "static/285661_star_icon.png";
    const textBoxDiv = document.createElement("div");
    textBoxDiv.classList.add("text-box");
    imgContainer.appendChild(starImg);
    imgContainer.appendChild(textBoxDiv);
    container.appendChild(imgContainer);
  }
}

//呈現頁面
function renderPage(value, times) {
  fetchData(url).then((spotInformation) => {
    const textBox = document.querySelectorAll(".text-box");
    const imgContainers = document.querySelectorAll(".img-container");
    // console.log(imgContainers);
    let count = 0;
    for (let i = value; i < value + times; i++) {
      // console.log(i);
      count += 1;
      //創建img tag
      const imgTag = document.createElement("img");
      imgTag.className = "picture";
      imgTag.src = spotInformation[i].image;
      imgContainers[i].appendChild(imgTag);
      //創建p tag
      const pTag = document.createElement("p");
      pTag.className = "small-text";
      pTag.textContent = spotInformation[i].Title;
      textBox[i].appendChild(pTag);
    }
    currentValue += count;
    if (currentValue >= 58) {
      loadMoreBtn.style.display = "none";
    }
  });
}

//初始化頁面
renderPage(currentValue, 13);
