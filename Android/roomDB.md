## 첫 번째. Android Room DB로 간단한 database 만들기


0. Dependencies 추가
    
    Gradle Scripts의 build.gradle(app)에서 다음 plugin과 dependency를 추가해 준다.
    ```
    plugins {
    id 'com.android.application'
    id 'kotlin-android'
    id 'kotlin-kapt'           // 추가된 부분
    }
    ```
    ```
    dependencies {
    
    // Room DB  
    implementation "androidx.room:room-runtime:2.3.0"       //추가된 부분
    implementation "androidx.room:room-ktx:2.3.0"           //추가된 부분
    kapt "androidx.room:room-compiler:2.3.0"                //추가된 부분
    }
    ```
    추가한 후 sync now를 눌러 준다.
<br /><br />
1. Model 만들기

    새로운 Kotlin class를 생성해 주고, 분류하기 쉽게 model 패키지를 만들어서 따로 넣어준다.

    ```Kotlin
    @Entity(tableName = "TABLE_NAME")
    data class TABLE_NAME(
        @ColumnInfo(name = "COLUMN_A")
        val COLUMN_A: TYPE_A,
        @ColumnInfo(name = "COLUMN_B")
        val COLUMN_B: TYPE_B
    ){
        @PrimaryKey(autoGenerate = true)
        val id: Int = 0
    }
    ```
    각 column은 table에 저장될 정보의 attribute가 된다. 원하는 column의 개수 만큼 ```@ColumnInfo```를 이용해 추가해 준다.
<br /><br />
2. Dao 만들기

    Dao는 Data Access Object의 약자로, 위에서 만든 table에서 할 수 있는 작업들(예: 원소 추가, 삭제, 불러오기 등)을 작성하는 곳이다.
    
    새로운 Kotlin **interface** class를 생성해 준다. Dao는 db 패키지를 만들어서 분류해 주면 좋다.
    ```Kotlin
    @Dao
    interface DAO_NAME {
        @Query(WHAT_TO_DO)
        fun FUNCTION_1(...) : ...
        
        @Delete
        suspend fun FUNCTION_2(...)
    }
    ```
    
    Annotation으로 어떤 작업을 할지 표시해 준다. ```WHAT_TO_DO```라고 쓴 곳에는 
    ```Kotlin 
    SELECT, FROM, DELETE FROM
    ```
    등 여러 명령어를 넣을 수 있다.
    이 함수들은 이후 생성할 Repository에서 사용하게 된다.
<br /><br />
3. Database 만들기
    
    새로운 Kotlin class를 db 패키지에 생성해 준다.
    
    1,2에서 생성한 model과 dao의 이름을 예를 들어서 각각 ```Jutak```과 ```JutakDao```로 한다.
    ```Kotlin
    @Database(entities = [Jutak::class], version=1)
    abstract class JutakDatabase : RoomDatabase() {
        abstract fun jutakDao(): JutakDao

        companion object {
            @Volatile
            private var INSTANCE: JutakDatabase? = null

            @JvmStatic
            fun getInstance(context: Context): JutakDatabase = INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    JutakDatabase::class.java,
                    "jutak_db"
                ).build().also {
                    INSTANCE = it
                }
            }
        }
    }
    ```
    프로그램 전체에서 객체가 딱 하나만 생기도록 하는 디자인 패턴인 Singleton pattern으로 만들어 준다.
<br /><br />
4. Repository 만들기

    repository는 방금 만든 local DB나 네트워크에서 정보를 받아와서, user가 사용하는 View나 ViewMode과 연결시켜 준다.
    
    repository 패키지를 만들고 새로운 Kotlin class를 생성해 준다.
    ```Kotlin
    class JutakRepository(private val jutakDao: JutakDao) {

        fun FUNCTION_1(...) = jutakDao.FUCTION_1
        suspend fun FUNCTION_2(...) = jutakDao.FUNCTION_2
        
        companion object {
            @Volatile
            private var INSTANCE:JutakRepository? = null

            @JvmStatic
            fun getInstance(jutakDao: JutakDao): JutakRepository = INSTANCE ?: synchronized(this) {
                INSTANCE ?: JutakRepository(jutakDao).also {
                    INSTANCE = it
                }
            }
        }

    }
    ```
    잘 읽어보면, repository 클래스는 Dao 객체를 받아서 생성된다. 그 내부에서는 Dao에서 정의했던 function들을 이용해서, 이제는 더 윗 레벨에서 사용할 function들을 정의한다.
    companion object 부분은 역시 Singleton한 구현을 위한 디자인 패턴이다.
<br /><br />
5. Application에서 연결시키기

    데이터베이스에 저장될 정보의 type과 같은 ```Model```, 사용 설명서와 같은 ```Dao```, 저장소와 같은 ```Database```, 그리고 소통 창구와 같은 ```Repository```를 만들었다.
    이제 이들을 가장 상위 레벨에서 묶어 줘야 한다. 이번 과제에서는 Application이 가지고 있도록 한다.
   
   새로운 Kotlin class를 만들어 준다. 
   ```Kotlin
    class App : Application() {

        private val jutakDatabase by lazy { JutakDatabase.getInstance(this) }
        val jutakRepository by lazy { JutakRepository.getInstance(jutakDatabase.jutakDao()) }

        override fun onCreate() {
            super.onCreate()
        }
    }
    ```
    App은 database를 private val로 갖고, repository도 val로 갖는다. 4번에서 했듯 repository 객체를 만들 땐 Dao를 parameter로 해서 만드는 것을 확인할 수 있다.
