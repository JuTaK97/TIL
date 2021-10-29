# OkHttp, Retrofit, Moshi를 이용한 간단한 네트워크 구조 만들기
[RecyclerView2] 에 이어지는 내용이다.<br />
http 통신으로 json 형태의 데이터를 받아와서 앞에서 구축한 DB에 저장해 본다.
## 1. Retrofit 구성하기
Retrofit 라이브러리는 Http 통신을 간편하게 할 수 있게 해준다. 라이브러리를 사용하지 않으면 
HttpURLConnection이라는 원시적인 방법으로 해야 하는데, 이 방법은 자유도가 높은 대신 모든 것을 직접 구현해야 한다.<br />
복잡한 Http 통신을 쉽게 해 주는 라이브러리가 OkHttp이고, 이를 기반으로 Retrofit 라이브러리가 만들어 져 있다.<br /><br />
사용하기 전에 먼저 dependency를 추가해 준다. 이번 과제에서 사용할 관련 depencency는 다음과 같다.
```Kotlin
// OkHttp
implementation "com.squareup.okhttp3:logging-interceptor:4.9.1"

// Retrofit
implementation 'com.squareup.retrofit2:retrofit:2.9.0'
implementation 'com.squareup.retrofit2:converter-moshi:2.9.0'

// Moshi
implementation 'com.squareup.moshi:moshi-kotlin:1.11.0'
```
Retrpofit 객체는 현재 프로젝트에서 가장 상위인 App.kt에 만들어 준다.<br />
```Kotlin
private val retrofit: Retrofit by lazy {
    Retrofit.Builder()
        .client(httpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .baseUrl(BuildConfig.BASE_URL)
        .build()
}
```
내용을 살펴보면, ```httpClient```, ```moshi```, ```BASE_URL```로 되어 있다. 하나씩 만들어 보자.<br />
httpClient는 다음과 같이 만들어 준다. OkHttpClient 객체이다.
```
private val httpClient: OkHttpClient by lazy {
    OkHttpClient.Builder()
        .addInterceptor(
            HttpLoggingInterceptor().apply {
                level =
                    if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY
                    else HttpLoggingInterceptor.Level.NONE
            }
        )
        .build()
}
```
moshi는 다음과 같이 만들어 준다. Moshi 객체이다
```
private val moshi: Moshi by lazy {
    Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()
}
```
마지막으로 BuildConfig.java에서 
```
public static final String BASE_URL = "json_정보를_받아올_https://어쩌구_URL";
```
와 같이 http 통신의 대상이 될 곳의 URL을 적어 준다.<br />
## 2. 데이터 받아오기
DB에 정보를 저장하거나 받아오기 위해 DAO를 썼듯, retrofit을 사용하기 위해서 Retrofit Service가 필요하다.<br />
새로운 인터페이스 클래스 MemberService.kt를 만들어 준다. <br />
먼저 만들어 줄 함수는 모든 정보를 받아오는 함수이다.
```Kotlin
interface MemberService {
    @GET("/waffle/members")
    suspend fun fetchAllMember(): FetchAllMemberResponse
```
이때 "/waffle/members"는 BASE_URL 위로 추가로 접근하는 부분이다. 이 경로에 있는 json을 @GET을 통해 모두 가져오게 된다. <br />
Retrofit의 장점은 원하는 형태의 객체로 정보를 받아올 수 있다는 것이다. ```fetchAllMember()``` 함수의 리턴 자료형이 ```FetchAllMemberResponse```인데, 이 클래스는 이렇게 되어 있다.
```Kotlin
data class FetchAllMemberResponse(
    val statusCode: Int,
    val body: List<Member>
)
```
순서대로 statusCode를 나타내는 Int와 body 내용인 List<Member> 형태의 객체로 받겠다는 뜻이다. 앞에서 만들었던 Member는 id, name, team, profile_image, lecture 등을 column으로 가지는 데이터 클래스였다. 실제로 정보를 받아올 URL에 들어가 보면, 
```Kotlin
{"statusCode":200,"body":[{"id":1,"name":"beomso0","team":"waffle"},...,{"id":12,"name":"jubilant-choi]","team":"iOS"}]}
```
처럼 되어 있다. 받아올 정보가 어떤 형태로 되어 있는지 보고, 적절한 data class를 만들어서 받아오면 되는 것이다.<br /><br />
이렇게 완성한 함수 ```fetchAllMember()```는 Int 자료형의 정보 하나와 List<Member> 자료형의 정보 하나를 가지는 객체를 반환한다. 이제 이 함수를 사용해 보자.

명령의 흐름과 정보의 흐름을 다시 한번 생각해 보면, 최상위에서 MainActivity가 MainViewModel에게 명령을 내린다. MainViewModel은 Repository에게 명령을 내리고, Repository는 본인이 가지고 있는 RetrofitService의 함수를 이용해 정보를 받아와서 이를 DAO에게 넘긴다. 마지막으로 DAO는 Database에 정보를 저장한다.<br />
그리고 DB에 뭔가 새로 저장되면, 그걸 observe하고 있던 ViewModel과 MainActivity는 Adapter의 내용을 알아서 바꿀 것이다.<br />
#### 3-1. MainActivity
```onCreate()```함수 내에 
```
viewModel.fetchMemberList()
```
[RecyclerView2]: https://github.com/JuTaK97/TIL/blob/main/Android/4_RecyclerView2.md
