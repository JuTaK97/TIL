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
DB에 정보를 저장하거나 받아오기 위해 DAO를 썼듯, retrofit을 사용하기 위해서 Retrofit Service를 만들어 준다.<br />







[RecyclerView2]: https://github.com/JuTaK97/TIL/blob/main/Android/4_RecyclerView2.md
