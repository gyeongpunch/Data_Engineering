2024.07.09     KPT (Keep, Problem, Try)
========================================

Review
-----
Multiprocessing M1~M4까지는 간단하게 어제 다 끝냈다. 하지만 Queue.empty가 Multiprocessing에서 보장을 하지 않는다는 범규님의 말씀에 도움과 feedback을 받았다. 그래서 Loop문을 고쳐서 더욱 안전한 코드를 완성했다. 또한, Youtube 댓글을 Youtube API를 이용하여 크롤링하여 Sentiment를 분석하여 Word Cloud를 만들었다.


Business insight
----------------
Tweet dataset말고도 Dataset을 이용하여 웹 스크레이핑 후 Word Cloud를 만들어보았다. 추가적으로 해당 Data를 분석하여 business insight를 어떻게 만들어낼 수 있을지 팀 토의를 하였다. 다음은 Youtube 댓글 뿐만아니라 Team brainstorming을 통해 나온 의견들이다.

1.	차량 유튜브의 유튜버 국가 별 sentiment를 분석하여 sentiment가 positive가 많은 차량의 공장 설계를 해당 국가와 가깝게 진행하여 운송비, 유류비를 줄일 수 있다.

2.	Steam TOP 100 Game의 최근 review에 대한 CG, Story, 타격감, 이용 연령  variation 등에 대한 sentiment를 분석하여 게임을 만들 때, 제한된 자본에 대한 투자 분산을 최적화할 수 있다. (ex. 요즘은 스토리에 끌리는 유저가 많다는 분석이 있다. 게임 스토리 작가에 돈을 많이 투자하자.)

3.	커뮤니티의 실시간 베스트 갤러리의 Meme에 대한 sentiment를 분석하여 MZ세대들을 겨냥하는 광고에 이용할 수 있다. (충주시 고문관님이 광고에 사용하는 듯 MZ세대를 겨냥하는 광고를 잘 targeting 할 수 있다.)

4.	The New York Times, The Washington Post, The Wall Street Journal의 특정 기업의 최신 경제신문에 대한 Sentiment를 분석하여 지금 핫한 기업에 대한 주식 투자에 이용할 수 있다.

5.	Booking, Air Bnb, TripAdvisor와 같은 여행 Platfrom의 월별 Sentiment를 분석하여 해당 월에 긍정적인 Sentiment가 많은 여행지에 쏘카를 많이 배치하여 이용률을 높일 수 있다.

6.	유튜브 영상의 정보로 시청자의 국가 추정 (자막 제공 언어) -> 영상별 sentimenet 분석 및 선호하는 keyword 확인 (ex. i30의 경우 DCT가 positive word cloud에 존재) -> 지역별 선호도 차이가 큰 차종의 경우, 해당 지역과 가까운 위치에서 생산함으로써 물류 비용 절감


Keep
----
1. 오늘 Youtube API를 이용한 웹 스크래핑을 한 후, Sentiment를 분석하여 Word Cloud를 만들었다. 요구사항이 자세히 나와있지 않았지만 'Youtube API 이용'이라는 Solution을 도출하여 점점 Issue에 대응할 수 있는 힘이 길러지는 것같다.
2. 점점 Class에 친해지는 사람이 많아지는 점이 뿌듯하다. 이번 주면 조를 바꾼다고 하셨는데 아쉽기도 하면서 새로운 동료들과 조를 할 생각에 설레기도 한다.

Problem
-------
1. AWS EC2와 Docker를 사용해보지 않아서 다소 걱정이 된다. 집에가서 M6을 완전히는 아니더라도 Googling과 Youtube를 이용해서 간단하게라도 시도해볼 생각이다.

Try
---
1. 역시 기술적인 구현보다 Business Insight를 도출하는 것이 훨씬 어려운 것같다. 창의적인 생각은 멍 때릴 때 많이 나온다. 하지만 뇌를 완전히 이완하면 지금 무엇을 하고 있었는지도 까먹게 된다. 사고의 수축과 이완을 적절히 하여 탁월한 Business Insight를 도출해낼 생각이다.



