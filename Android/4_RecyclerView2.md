# 다양한 Viewtype을 이용해서 recyclerView 디자인하기
viewModel, roomDB, RecyclerView에 이어지는 내용이다.<br /><br />
여러 종류의 member의 정보를 recyclerView에 띄워보는 것을 구현해 본다. 이때 정보를 http를 통해 json 형식으로 받아 올 것이다.<br />
## 1. DB 구조 짜기(복습)
#### 1-1. data 
DB에 저장될 ```Member```은 ```id```, ```name```, ```team```, ```profile_image```, ```lectures```를 column으로 가지는 데이터이다.<br /> 
새로운 kotlin class Member.kt를 만들고 json으로 받아올 예정이니 annotation을 하나 더 붙여서,
```Kotlin
@JsonClass(generateAdapter = True)
@Entity(tableName = "member_table")
data class Member(
    @Json(name = "id")
    @ColumnInfo(name = "id") @PrimaryKey
    var id: Int,

    @Json(name = "name")
    @ColumnInfo(name = "name")
    var name: String,

    @Json(name = "team")
    @ColumnInfo(name = "team")
    var team: String,

    @Json(name = "profile_image")
    @Ignore
    var profileImage: String?,

    @Json(name = "lectures")
    @Ignore
    var lectures: List<Lecture>?
) {
    constructor():this(0, "", "", null, null)
}
```
와 같이 만들어 준다. ```@ignore```설명은 추후 추가<br /><br />
#### 1-2. DAO
MemberDao.kt를 만들고, ```member_table```에 요청할 여러 함수들을 만든다. 지금은 일단 가져오기 하나만 만들어 놓는다.<br />
```Kotlin
@Dao
interface MemberDao {

    @Query("SELECT * FROM member_table")
    fun getAllMember() : LiveData<<List<Member>>
}
```
#### 1-3. Database
MemberDatabase.kt도 만들어 준다. [roomDB.md]에서 한 것처럼 만들면 된다.<br />
#### 1-4. Repository
MemberRepositoty.kt는 private 객체로 Dao를 갖는다. 그리고 Dao의 함수와 사용자를 연결할 함수를 만들어 준다.<br />
```Kotlin
class MemberRepository constructor(
    private val memberDao: MemberDao,
    private val memberService: MemberService
    ) {
    
    fun getAllMember() = memberDao.getAllMember()
    suspend fun deleteMember() = memberDao.deleteMember()

    companion object {
        @Volatile
        private var INSTANCE: MemberRepository? = null

        @JvmStatic
        fun getInstance(memberDao: MemberDao, memberService: MemberService) =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: MemberRepository(memberDao, memberService).also { INSTANCE = it }
            }
    }
}
```
이때 Dao에서 database를 수정하는 함수들(insert, delete 등)은 꼭 suspend fun으로 작성해 주어야 한다.<br />
이제 roomDB의 구조를 완성했다.
## 2. 여러 viewType을 운용하는 Adapter 만들기
먼저, MemberAdapter.kt의 가장 기본적인 모습은 다음과 같다.
```Kotlin
class MemberAdapter : RecyclerView.Adapter<RecyclerView.ViewHolder>() {
    private var members: List<Member> = listOf()
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        
    }

    override fun getItemCount(): Int {
        
    }
}
```
viewType이 하나일 때는 inner class를 만들었는데, 여러 개면 그냥 여러 개의 inner class를 만들어 주면 된다.<br />
여러 viewType을 쓴다는 것은, 각각의 디자인을 담당하는 xml 파일들이 있다는 뜻이고 이것들을 각각 사용해 주면 된다.<br />
```Kotlin
inner class MemberType1ViewHolder(var binding : ItemMemberType1Binding): RecyclerView.ViewHolder(binding.root)
inner class MemberType2ViewHolder(var binding : ItemMemberType2Binding): RecyclerView.ViewHolder(binding.root)
```
이 경우 각각의 xml 파일 이름은 item_member_type1.xml 과 item_member_type2.xml이 되겠다. (xml의 파일 이름대로 하면 된다)<br /><br />
다음으로 ```onCreateViewHolder()``` 함수를 완성해 본다.<br />
viewType이 여러개이기 때문에, ```onCreateViewHolder()```의 생성자에서 받아온 Int타입의 ```viewType```에 따라 다른 return을 내야 한다.<br />
그런데 viewType이 하나일 때는 아무 상관 없었는데, 여러개가 되면 문제가 된다. 이때 필요한 것이 새로운 함수이다.<br />
```onCreateViewHolder()```가 override하는 함수는 필수로 저 위의 3개지만, 여러 다른 함수를 override할 수 있다. <br />
그중 하나가 지금 사용할 ```getItemViewType```이다.<br />
```Kotlin
override fun getItemViewType(position: Int): Int{
    return 0
}
```
```onCreateViewHolder()```가 불릴 때, 이 함수가 먼저 불려서 viewType을 받아온다. 디폴트 리턴값은 0인데 viewType을 여러 개 쓸거면 상황에 맞게 여러 값을 리턴시켜줘야 한다.
<br />이때 인자로 받는 ```position```은 member의 인덱스이다. 따라서 다음과 같이 할 수 있다.
```Kotlin
override fun getItemViewType(position: Int): Int{
    return when(members[position].team){
        "team1" -> 0
        "team2" -> 1
        ...
        else -> -1
    }
}
```
물론 지금 가정하고 있는 상황은 표시할 viewType의 member의 team의 종류에 따라 다르게 하는 것이다. return할 정수 값 자체는 맘대로 정해주면 된다.<br />
이제 다시 ```onCreateViewHolder```로 돌아가서, 
```Kotlin
override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
    return when(viewType){
        0 -> {
            val binding = ItemMemberType1Binding.inflate(LayoutInflater.from(parent.context), parent, false)
            MemberType1ViewHolder(binding)
        }
        1 -> {
            val binding = ItemMemberType2Binding.inflate(LayoutInflater.from(parent.context), parent, false)
            MemberType2ViewHolder(binding)
        }
        else -> throw IllegalStateException("Illegal viewType")
    }
}
```
viewType에 맞게 올바른 binding으로 만든 viewHolder를 반환해 주면 된다.<br /><br />
다음은 ```onBindViewHolder()```이다.
[recyclerView.md]에서 했던 것과 동일한데 경우를 나눈 것만 추가하면 된다.<br />
```Kotlin
override fun onBindViewHolder(holder : RecyclerView.ViewHolder, position: Int) {
    when(holder) {
        is MemberTeam1ViewHolder -> {
            holder.binding.apply {
                ...
            }
        }
        is MemberTeam2ViewHolder -> {
            holder.binding.apply {
                ...
            }
        }
    }
}
```
holder의 타입별로 나눠 주고, ```holder.binding.apply{}``` 안에는 구체적인 xml 파일 내에 디자인된 view들을 채우면 된다.<br />
예를 들면 item_member_team1.xml에 id가 text_name인 textView가 있다면 
```
textName.text = data.name
```
과 같이 해 주면 된다. 물론 ```name```은 member 데이터가 가지는 한 column이다.<br /><br />
## 3. MainActivity, MainViewModel과 연결하기(복습)
계속 해오던 대로, 가장 상위의 MainActivity에서는<br />
```Kotlin
override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        memberAdapter = MemberAdapter()
        memberLayoutManager = LinearLayoutManager(this)
        binding.recyclerViewMember.apply {
            adapter = memberAdapter
            layoutManager = memberLayoutManager
        }
        viewModel.observeMember().observe(this) {
            memberAdapter.setMembers(it)
        }
}
```
과 같이 viewModel에게 observeMember 시킨다음, 그 결과(```LiveData<>``` 형태)를 observe해서 그것(```it```)을 memberAdapter에게 전달한다.<br />
이 과정을 위해 viewModel은 ```fun observeMember() = memberRepository.getAllMember()``` 한줄이면 충분하고, Adapter는 
```Kotlin
fun setMembers(members : List<Member>) {
    this.members = members
    this.notifyDataSetChanged()
}
```
와 같은 함수를 추가해 주면 된다. ```this.notifyDataSetChanged()```를 통해 변경 사항을 업데이트 하게 된다.<br /><br />
이제 MVVM 구조를 활용한 아주 간단한 DB와 그것을 출력할 UI 구축이 완료되었다. 이제 정보를 http를 통해 받아오는 것을 다음 문서에서 공부해 본다.<br /><br />
    


[roomDB.md]: https://github.com/JuTaK97/TIL/blob/main/Android/2_roomDB.md
[recyclerView.md]: https://github.com/JuTaK97/TIL/blob/main/Android/3_RecyclerView.md
