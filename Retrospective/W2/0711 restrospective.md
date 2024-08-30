2024.07.11     KPT (Keep, Problem, Try)
========================================

Review
-----
오늘은 하루종일 Sentiment Analysis를 했다. 완전 획기적인 Business Insight를 도출하고 싶었는데 1차원적인 결론만 생각이 나서 조금 슬펐다. 결국은 자동차 Analysis로 돌아갔다. 또한 Airbnb라는 숙박 Platform을 크롤링하여 위치별, 테마별 Review의 Sentiment를 분석하고 싶었는데 이에 애로사항이 너무나도 많았다. 숙소 하나하나의 Review는 십수개에서 수십개로 다른 Platform보다는 Comment나 Review가 적었다. 그래서 최대한 많은 숙소에 대해 크롤링하고 싶었는데 Airbnb에서 스크롤로 load하다가 간헐적으로 button으로 load를 하게 만들어놨다. 또한 load button과 '지도 view' button이 같은 위치에 있어서 애로사항이 있었다. 그래서 youtube돌아가서 내가 직접 comment를 정제를 했다.

Keep
----
1. Airbnb를 크롤링하기에 애로사항이 있었지만 계속 해보려는 시도, 늦지 않게 youtube로 다시 돌아간 판단이 좋았다고 생각한다. 제한된 시간동안 한 가지 일에 계속 낑낑거리는 것은 나의 스타일이 아닌 것 같다. 다음날 아침에 보면 해결할 수 있는 아이디어가 떠오른 적이 적지 않기 때문이다. 하지만 지금의 Project는 시간이 촉박하다. 그래서 그저께 했던 Youtube로 돌아갔다. 그래도 Airbnb를 너무 적게 찍먹만 하지 않았던 점, 나의 경험을 살려 Youtube를 이용하여 Sentiment Analysis로 돌아간 판단은 좋았다고 생각한다.

Problem
-------
1. Airbnb를 완벽하게 크롤링하는 데에 실패했다. Selenium을 이용하여 스크롤을 내리다가 간헐적으로 등작하는 'More Review' Button에 맞게 동작하게 하고 싶었지만 지금 뇌가 많이 지쳤는지 코드가 잘 안 짜졌다. 그래서 과감하게 Youtube comment analysis로 돌아갔다. 불현듯 좋은 아이디어가 떠오르면 추후에 다시 시도해봐야겠다. 왜나하면 Airbnb뿐만 아니라 많은 Platform에서도 충분히 일어날 수 있는 상황이라 생각되어 나중에 부딪힐 문제라고 생각되기 때문이다.

Try
---
1. 점점 할 게 많아지는 것 같다. PR할 Project file도 최적화해야하고 AWS, Docker도 공부해야하고 지금의 Project인 Sentiment Analysis도 마무리 해야하고 각오했던 경영학책도 읽어야한다. 우선 이동하는 시간에는 독서와 AWS, Docker 공부가 가장 알맞는 것 같다. 이동시간이 짧은 편도 아니니까 독서도 하고 Youtube영상을 보며 AWS, Docker 공부를 해야겠다. 그리고 Deadline과 중요도를 설정하여 해야할 일을 Scheduling해야겠다. 내가 부여한 Priority 순서대로 할 일을 끝내야겠다.

</br>

## Predicting Election Results from Twitter Using Machine Learning Algorithms_Report
기존의 사전 조사나 전문가 의견에 의존하는 대신, 소셜 미디어통해 실제 사용자들의 트윗을 분석하여 정치적 성향을 파악하고 이를 통해 선거 결과를 예측하는 방법을 제안하고 있다.

읽자마자 영화 '더킹'이 생각났다. 영화에 따르면 대통령이 누가 당선될지에 따라 많은 사람의 밥줄이 달려있다. 기존에 자신의 정치적 견해, 약간의 운에 의존했다면 지금은 이러한 점들을 철저히 통계학적으로 계산할 수 있다는 점이 고무적이다.

미래에는 이 기술이 훨씬 발전했을 것이며, 이로 인해 정치인들은 트위터를 비롯한 소셜미디어에서 활발히 활동하는 MZ세대의 눈치를 약간이라도 더 많이 볼 것으로 기대된다.

이에 따라 더욱 유의미한 청년정책 또한 내놓을 것이라 기대할 수 있다.