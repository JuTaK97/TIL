## RecyclerView로 간단한 앱 만들기

[RoomDB.md]에서 이어지는 내용이다.


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
<br /><br />
  repository는 DB와 View의 소통 창구이다. MainViewModel에 repository를 생성해 준다.
  ```Kotlin
  private val jutakRepository by lazy { (application as App).jutakRepository }
  ```
  그리고 repository에 만들었던 함수를 써먹기 위해 함수들을 만든다.

  - 종류 1:   그냥 fun<br />
    repository에서 그냥 fun이었던 함수는 별 다를게 없다.<br />
    ```fun FUNCTION_1() = jutakRepository.FUNCTION_1()```
    이렇게 이어주면 된다.<br /><br />
  - 종류 2:   **suspend fun**<br />
    repository에서 suspend fun이었던 함수는 다음과 같이 한다.
    ```
    fun FUNCTION_2(...) {
            viewModelScope.launch {
                jutakRepository.FUNCTION_2(...)
            }
        }
    ```
    <br />
    이제 RecyclerView를 구현하기 위한 준비가 끝났다.<br /><br />
    
## 1. Adapter 만들기

새로운 Kotlin 클래스 JutakAdapter를 만들어 준다.
```Kotlin
class JutakAdapter : RecyclerView.Adapter<JutakAdapter.JutakViewHolder>(){

    inner class JutakViewHolder(val binding:ItemJutakBinding) :
        RecyclerView.ViewHolder(binding.root)
}
```
 ```ItemJutakBinding```은 Jutak이라는 타입의 객체가 View에서 어떻게 표시될 것인지를 나타내는 xml 파일과 관련되어 있다.<br />
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
이제 Adapter를 만들었으니 MainViewModel 등과 연결시켜야 한다.<br /><br />
## 2. MainActivity에 Adapter 만들기

MainActivity 클래스에 adapter를 선언해 준다.
```Kotlin
private lateinit var jutakAdapter: JutakAdapter
private lateinit var jutakLayoutManager: LinearLayoutManager
```
그리고 onCreate() 함수 안에 lateinit들을 마저 선언해 준다.
```Kotlin
jutakAdapter = JutakAdapter()
jutakLayoutManager = LinearLayoutManager(this)
binding.recyclerViewJutak.apply{
      adapter = jutakAdapyer
      layoutManager = jutakLayoutManager
}
```
아직 activity_main.xml에 recyclerView를 넣어주지 않았으면, ```recycler_view_jutak```을 id로 갖는 recyclerView를 추가해 준다.<br /><br />
## 3. XML 파일 디자인하기

먼저 ```item_jutak.xml```을 만들어 본다.<br /><br />
jutak은 title과 content라는 두 column을 가지는 자료라고 하자. 그러면 title과 content를 표시할 TextView를 마련해 주자.<br />
그리고 그 View를 삭제할 때 쓸 버튼을 하나 만든다.
```Kotlin
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    ...기타등등 설정들 >

    <TextView
        android:id="@+id/text_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" 
        ...기타등등 설정들 />

    <TextView
        android:id="@+id/text_detail"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        ...기타등등 설정들 />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        ...기타등등 설정들 >
    </Button>
</androidx.constraintlayout.widget.ConstraintLayout>
```
이제 ```JutakAdapter```에 남겨두었던 ```onBindViewHoder``` 함수를 완성할 수 있다.
```Kotlin
    override fun onBindViewHolder(holder: TodoViewHolder, position: Int) {
        val data = todos[position]
        holder.binding.apply {
            textTitle.text = data.title
            textDetail.text = data.content
        }
    }
 ```
이처럼 item_jutak.xml의 TextView들의 id를 따라가서 text를 넣어 줄 수 있다.<br /><br />
그 다음으로 activity_main.xml을 디자인 해 본다.
LinearLayout 하에 recyclerView 하나를 넣어 주고, View 추가용 floating button 하나를 넣어 주었다.
```Kotlin
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ui.MainActivity"              //중요
    android:orientation="vertical">
    
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recycler_view_todo"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        tools:listitem="@layout/item_todo"
        />
    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/addButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_marginEnd="16dp"
        android:layout_marginBottom="16dp"
        app:srcCompat="@android:drawable/ic_input_add" />
</LinearLayout>
```
이제 프로젝트의 모든 틀이 마무리되었다.
## 4. 동작 추가하기
이제 setOnClicker 등을 이용하여 구체적인 구현을 해 본다.

해야할 것은 총 3가지이다.
1. activity_main.xml에 만든 추가하기 버튼 구현
2. item_jutak.xml에 만든 삭제하기 버튼 구현
3. MainViewModel이 LiveDate를 observe하고 표시되는 것을 update.
<br /><br />
## 4-1. RecyclerView에 view를 추가하는 버튼
버튼을 눌렀을 때 입력을 받아줄 대화상자가 뜨게 해 본다.<br />
ActivityMain에 다음 함수를 추가한다.
```Kotlin
private fun showDialog() {
    val dialogBinding = DialogAddTodoBinding.inflate(layoutInflater)
    val dialogBuilder = AlertDialog.Builder(this)
        .setTitle("Add Todos")
        .setView(dialogBinding.root)
        .setPositiveButton("create") { _, _ ->
            viewModel.addTodo(
                dialogBinding.dialogTextTitle.text.toString(),
                dialogBinding.dialogTextContent.text.toString()
            )
            Toast.makeText(applicationContext, "Create", Toast.LENGTH_SHORT).show()
        }
        .setNegativeButton("cancel") { _, _ ->
            Toast.makeText(applicationContext, "Cancel", Toast.LENGTH_SHORT).show()
        }
    val dialog = dialogBuilder.create()
    dialog.show()
}
```
그리고 대화상자의 디자인을 담당할 ```dialog_add_todo.xml```을 만들어 준다.
```Kotlin
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <EditText
        android:id="@+id/dialog_text_Title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"/>
    <EditText
        android:id="@+id/dialog_text_Content"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"/>
</LinearLayout>
```
이제 ActivityMain의 onCreate 안에 setonclicker를 설정해준다.
```Kotlin
binding.addButton.setOnClickListener {
    showDialog()
}
```
## 4-2. RecyclerView에서 view를 삭제하는 버튼


[RoomDB.md]: https://github.com/JuTaK97/TIL/blob/main/Android/roomDB.md
