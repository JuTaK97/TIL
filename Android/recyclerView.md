## RecyclerView로 간단한 앱 만들기

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
<br />
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
    
## **1. Adapter 만들기**

새로운 Kotlin 클래스 JutakAdapter를 만들어 준다.
```Kotlin
class JutakAdapter : RecyclerView.Adapter<JutakAdapter.JutakViewHolder>(){

    inner class JutakViewHolder(val binding:ItemJutakBinding) :
        RecyclerView.ViewHolder(binding.root)
}
```
 ```ItemJutakBinding```은 Jutak이라는 자료가 View에서 어떻게 표시될 것인지를 나타내는 xml 파일과 관련되어 있다.<br />
 res 폴더의 layout 폴더에 새 xml 파일을 만들어준다. 이름은 item_jutak.xml이 되면 된다. 세부적인 디자인은 나중에 하면 된다.<br /><br />
 이제 JutakAdapter 클래스가 RecyclerView의 Adapter로 작동할 수 있도록 멤버 함수들을 구현해야 한다.<br /><br />
 그 전에, Adapter가 정보들(Jutak 객체들)을 담아 둘 공간이 필요하다. 
 ```private var jutaks: List<Jutak> = listOf()```를 생성해서 공간을 만들어 준다.<br /><br />
 이제 빨간 줄이 쳐져 있을 클래스 이름을 우클릭 해서 세 필수 함수를 가져와서 작성한다.
 ```Kotlin
     override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): JutakViewHolder {
        val binding = ItemJutakBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return JutakViewHolder(binding)
    }
    
    override fun getItemCount() = jutaks.size
    
    override fun onBindViewHolder(holder: JutakViewHolder, position: Int) {
        val data = memos[position]
            holder.binding.apply {
                // TODO : xml 파일 디자인 이후
        }
    }
```
RecyclerView에 표시할 여러 값들을 담는 곳이 ```holder```가 되고, 각 ```position```에 대해 어떻게 담을지 설정하는 함수가 바로 ```onBindViewHolder```이다.<br />
함수 내부에서는 ```item_jutak.xml```내부에 디자인한 TextView 등의 여러 자리에 ```val data```의 값들을 가져와서 알맞게 적용시키게 된다. <br /><br />예시로,
```Kotlin
textTitle.text = data.title
```
```item_jutak.xml```에 있는 textView의 id인 ```textTile```의 text를 ```data.title```로 바꿔주는 것이다. 물론 이때 ```title```은 ```Jutak```의 한 column이다.<br /><br />
이제 Adapter를 만들었으니 MainViewModel 등과 연결시켜야 한다.
