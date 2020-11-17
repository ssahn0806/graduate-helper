# graduate-helper
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
광운대학교 소프트웨어학부생들에게 KLAS의 수강/성적 Data를 추출하여 

졸업요건을 만족하기 위해 남은 이수학점을 영역별로 알려드립니다.

Python 언어, ChromeDriver 로 설계되었기에 동작을 위해서는 Python 3.8.X , Chrome 의 설치가 필요합니다.

## 기여
[여기](https://github.com/ssahn0806/graduate-helper/blob/main/CONTRIBUTING.md)를 참고해 주세요.

## 프로젝트 내용
Python의 Selenium과 Requests 모듈을 활용, ChromeDriver를 통해 KLAS 에 접속하고 조회일 기준 학기까지의 수강/성적 Data를 추출한 뒤

학번에 따른 소프트웨어학부 졸업기준, 공학프로그램 기준을 얼만큼 만족하는지 판단하여 잔여 학점을 영역별로 상세하게 알려드립니다. 

## 환경 설치
1. Python 3.8.X 설치 [다운로드](https://www.python.org/downloads/)
2. Chrome 실행 후 다음을 입력하여 version 확인 (chrome:://version)
3. version에 맞는 ChromeDriver 설치 [다운로드](https://chromedriver.chromium.org/downloads)
4. 다음 명령어들을 활용하여 필요한 패키지,모듈 설치
* pip install selenium
* pip install requests
* pip3 install PyQt5

## 사용 방법
1. src 폴더 전체를 로컬에 다운로드 합니다.
2. 본인의 chrome 환경에 맞게 다운로드한 chromedriver.exe 파일을 해당 폴더[src]에 복사합니다.
3. main.py를 더블클릭하여 실행합니다.
4. 초기 UI화면에 KLAS에 등록된 학번과 비밀번호를 입력 후 수강 확인 버튼을 클릭합니다.
5. 로그인 정보가 올바를 경우 수초내에 팝업창을 통해 안내하며, 콘솔창에는 현재까지 수강한 과목의 정보가, UI창에는 남은 학점의 수치가 나타납니다.

* 본 실행 방법은 프로그램 최초 실행시 도움말 버튼을 통해 확인하실 수도 있습니다.

## 필독
* 이 프로젝트는 '오픈소스소프트웨어개발' 수업의 결과물로 제작되었으며, 광운대학교 소프트웨어학부 학생들의 수강 데이터만 처리하도록 설계되었습니다.
#### 안내
* 입력하는 학번과 비밀번호는 로그인과 성적정보를 추출하기 위해서만 활용되고, 본인의 로컬환경에서 실행되므로 안심하고 사용하셔도 됩니다.
#### 이용대상
* 우선적으로 소프트웨어학부로 입학한 16학번 이상의 학생들을 이용 가능 대상으로 합니다.
#### 기능
1.기존 KLAS의 공학프로그램 이수현황과 수강/성적 조회를 별도로 확인해야하는 점

2.기존 KLAS의 수강/성적 조회에서는 성적처리가 마감된 정보를 대상으로 제공하는 점

3.16~18 학번의 대학영어 필수/면제여부를 어학성적조회를 통해 확인해야 하는 점

위의 불편사항을 개선하여 모든 정보를 한꺼번에 제공합니다.

* 졸업기준을 달성하기 위한 필수교양/균형교양/기초교양/전공/이수 총학점 

  공학인증 기준학점과 현재까지 이수학점, 잔여학점 제공
* 현재까지의 수강한 과목 영역별 제공

#### 영역별 분류기준
영역별 이수 기준은 수강신청자료집의 학번별 졸업이수요건과 인정과목을 기준으로 합니다. 

자세한 내용은 수강신청자료집을 참고하시기 바랍니다.

* 필수교양의 경우 학번, 레벨테스트 면제여부에 따라 기준학점이 정해집니다.
* 균형교양의 경우 학번에 따라 기준학점이 정해지며, 

  수강신청자료집에서 균형교양으로 인정하는 과목에 대해서만 계산합니다. 
  
  이를 만족하지 않는 교양과목은 교양선택으로 분류하였습니다.
#### 결과 해석
재수강하여 삭제되었거나 미이수(F 또는 NP) 과목은 계산되지 않으며, 

조회시점에 따라 수강/성적조회에 표시되는 현재 재학중인 학기(성적처리 X)까지 데이터를 포함하여 계산된 결과이므로 

주어진 정보를 통해 남은 학기동안의 수강신청 계획을 세울 수 있습니다.
#### 주의사항
* 각 영역별 DB는 소프트웨어학부 졸업요건을 기준으로 하여, 타학과 학생의 결과의 정확도는 보장될 수 없습니다.
* 이 프로젝트에서 제공하는 정보는 개인적인 확인 용도로 사용을 권장하며, 공식적인 근거자료로 활용될 수 없습니다.
* 배포 초기에는 표본이 부족하여 결과가 정확하지 않을 수도 있습니다.

## 부족한 점
* 실행 결과가 정확하지 않다면 [여기](https://github.com/ssahn0806) 에 등록된 이메일로 알려주세요.
* 16학번 이전의 졸업기준은 정보 수집의 한계로 여러분의 도움을 기다리고 있습니다.[기여](https://github.com/ssahn0806/graduate-helper/blob/main/CONTRIBUTING.md)
* MIT license 를 준수한다면 타학과에서 얼마든지 이용가능하도록 설계하였습니다.[활용방법](https://github.com/ssahn0806/graduate-helper/blob/main/APPLICATION.md)





## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/ssahn0806"><img src="https://avatars2.githubusercontent.com/u/28581673?v=4" width="100px;" alt=""/><br /><sub><b>ssahn0806</b></sub></a><br /><a href="#projectManagement-ssahn0806" title="Project Management">📆</a> <a href="https://github.com/ssahn0806/graduate-helper/commits?author=ssahn0806" title="Code">💻</a> <a href="#ideas-ssahn0806" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/csh970605"><img src="https://avatars0.githubusercontent.com/u/28240052?v=4" width="100px;" alt=""/><br /><sub><b>Choi_Se_Hoon</b></sub></a><br /><a href="#design-csh970605" title="Design">🎨</a> <a href="https://github.com/ssahn0806/graduate-helper/commits?author=csh970605" title="Code">💻</a></td>
   <td align="center"><a href="https://github.com/Wjaehyun"><img src="https://avatars1.githubusercontent.com/u/72908405?v=4" width="100px;" alt=""/><br /><sub><b>Wjaehyun</b></sub></a><br /><a href="https://github.com/ssahn0806/graduate-helper/commits?author=Wjaehyun" title="Data">🔣</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
