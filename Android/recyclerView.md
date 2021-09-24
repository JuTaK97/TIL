## RecyclerView로 간단한 일정 앱 만들기

roomDB.md에서 이어지는 내용이다.


## **0. MainActivity와 MainViewModel 만들어 주기**

  먼저 원래 하던 것처럼, binding을 위해서 gradle(app)에 
  ```Kotlin
  android {
      ...
      buildFeatures {
              viewBinding = true
          }
  }
  ```
  을 추가해 준다.

  MainActivity에 ```private lateinit var binding : ActivityMainBinding```를 선언해 주고,<br />
  Oncreate 함수 안에는 ```binding = ActivityMainBinding.inflate(layoutInflater)``` 로 lateinit를 해소해 준다.<br />
  그리고 setContentView 안을 R.어쩌구 에서 ```binding.root``` 로 바꿔 준다.

  roomDB를 만들 때 App class를 만들어 줬었다. 
  따라서 MainViewModel의 첫 부분을<br />
  ```class MainViewModel(application: Application) : AndroidViewModel(application){``` 로 바꿔 준다.
  AndroidViewModel이 바로 application context를 사용할 수 있게 해주는 class이다.

  repository는 DB와 View의 소통 창구이다. MainViewModel에 repository를 생성해 준다.
  ```Kotlin
  private val jutakRepository by lazy { (application as App).jutakRepository }
  ```
  그리고 repository에 만들었던 함수를 써먹기 위해 함수들을 만든다.

  - 종류 1: 그냥 fun
    repository에서 그냥 fun이었던 함수는 별 다를게 없다.<br />
    ```fun FUNCTION_1() = jutakRepository.FUNCTION_1()```
    이렇게 이어주면 된다.<br />
  - 종류 2: **suspend fun**
    repository에서 suspend fun이었던 함수는 다음과 같이 한다.
    ```
    fun FUNCTION_2(...) {
            viewModelScope.launch {
                jutakRepository.FUNCTION_2(...)
            }
        }
    ```<br />
    이제 RecyclerView를 구현하기 위한 준비가 끝났다.<br /><br />
    
## **1. RecyclerView 만들어보기**
