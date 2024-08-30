2024.07.10     KPT (Keep, Problem, Try)
========================================

Review
-----
오늘은 W1의 M1인 mtcars dataset를 analysis한 ipynb file에 대한 Docker Container Image를 생성하고 AWS EC2에 배포했다. 오늘이 근 열흘동안 가장 어려웠던 것같다. 어떠한 프로그래밍 로직이 필요한 것이 아니라 AWS의 manual을 잘 따라가면서 EC2에 배포해야하는데 경우의 수도 너무 많고 구글이 하라는대로 그저 따라만하다가 시간이 다 가버려서 다소 회의감이 들었다. 세상에는 알아야하는 것이 너무나 많은 것같다. AWS를 하다가 sentiment analysis를 할 시간이 매우 촉박해졌다. 오늘 AWS setting, method 등을 빠르게 정리하고 내일은 기존에 Team brainstorming에 추가로 생각한 것들에 대해 Sentiment analysis를 해봐야겠다.

Keep
----
1. 오늘 생소한 AWS와 Docker를 다루면서 너무나 기능이 많아서 길을 헤맸는데, Notion으로 나만의 Manual을 만들면서 정리했다. Project Code 뿐만 아니라 이러한 Manual을 하나하나 기록하다보면 이 또한 큰 자산이 될 것이라는 생각이 들었다. 앞으로도 생소한 Tool에 대해서 Munual을 차근차근 정리해봐야겠다.

Problem
-------
1. 어제 회고에 "AWS EC2와 Docker를 사용해보지 않아서 다소 걱정이 된다." 라고 작성했는데 아니나 다를까 구글에서 Manual을 검색한다고 애를 먹었다. Docker와 AWS에 관한 Blog를 많이 읽으면서 대부분의 기능은 아니더라도 조금의 기능은 익혀둘 생각이다.
2. Youtube 댓글이 생각보다도 더 Quality가 떨어지는 것같다. 짧은 시간에 Sentence를 정제해서 Word Cloud로 만드는 Model을 개발하기에는 어렵고 이미 만들어진 Model을 사용해야할 것같다. 그러기엔 Youtube의 댓글이 이 Model에 fit하다는 생각이 들지않는다. 조금 더 comment들이 정제되어있는 Platform에서 웹 스크래핑하여 Sentiment Analysis하기에 더 fit한 Data를 모아볼 생각해야겠다.

Try
---
1. Review에도 말했듯 AWS와 Docker에 대한 지식, 경험이 많이 부족하다고 생각한다. 그래서 이리저리 건드려보고 Blog도 읽으면서 더 친숙해져봐야겠다.
2. Data Engineering은 아주아주 폭 넓은 지식과 Insight가 필요한 것같다. 그래서 경영학책을 빌렸다. 하루에 최소 10페이지는 읽으면서 소위말하는 문과적인, 인문학적인 지식을 함양할 생각이다.