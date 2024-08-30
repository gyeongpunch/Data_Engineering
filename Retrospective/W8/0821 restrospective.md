2024.08.21     KPT (Keep, Problem, Try)
========================================

Review
-----
* 이제이제 진짜 거의 다 완성했다. EMR 전처리부터 graph_score를 구하고 View Table로 만든 뒤에 Chart.js를 이용하여 웹에 Plot하였다. Hot Issue 탭에서는 Trigger Detect된 Car-Issue 사례에 대해 DTW를 이용하여 유사성이 높은 사례를 그룹핑했고 같이 Plot하게 하였으며 사례들이 서로 다른 경향성을 보여주는 것도 있고 아닌 것도 존재함을 확인했다. 이제 Trigger 테이블에 넣을 때 해당 car-issue에 대해 웹서버에 api만 호출하여 알림만 주면 된다. 이건 아마 오늘 중으로 할 수 있지 않을까 기대된다.

Keep
----
1. 

Problem
-------
1. 모델링을 어떻게 하냐에 따라 Hot Issue Trigger에 해당하는 모니터링 Car-Issue가 다를텐데 이것을 더 최적화해야겠다.

Try
---
1. 