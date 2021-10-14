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
    fun getAllMember() : LiveData<Member>
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
이 경우 각각의 xml 파일 이름은 item_member_type1.xml 과 item_member_type2.xml이 되겠다. (xml의 파일 이름대로 하면 된다)<br />
다음으로 ```onCreateViewHolder()``` 함수를 완성해 본다.


[roomDB.md]: https://github.com/JuTaK97/TIL/blob/main/Android/2_roomDB.md
