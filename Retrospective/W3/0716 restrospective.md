2024.07.16     KPT (Keep, Problem, Try)
========================================

Review
-----
오늘은 팀원들과 사이드 프로젝트 주제를 어제보다 더욱 추리고, 추린 주제에 대해 구체화했다. 처음 아이디어보다 더 발전된 것이 느껴진다.
또한, Hadoop과제를 진행했다. Dockerfile을 만들과 이에 필요한 xml, sh 파일을 작성하여 Docker Image를 만들고 Container를 실행시키고 HDFS를 만드는 것까지 성공했다. 하지만 과제에서 요구하는 방향과 다소 다른 방법으로 진행한 것같아서 Dockerfile을 다시 수정하여 과제를 진행했다. 하지만 Dockerfile을 수정하니까 부가적인 error가 많이 나오고 있는 상황이다. 디버깅하는 것은 시간박치기로 할 수 있을 것같아서 집에 가서도 디버깅을 해보고 이래도 error를 못 잡는 것은 팀원에게나 다노님에게 질문해야겠다.

Keep
----
1. 

Problem
-------
1. 처음에 Dockerfile에서 build하고 container를 실행시키고 HDFS를 fomatting하였다. user hadoop을 만들고 file을 read하려고 하는데 file은 분명히 있는데 읽어오지 못해서 터미널에서 hadoop에게 Read 권한 등 file access 권한을 부여해주면서 과제를 진행했다. 하지만 이것은 다소 Dockerfile을 작성하는 의미가 떨어지는 것같아 Dockerfile에 모든 과정을 담아서 터미널에 기본적인 작동 commend만 작성하면 가능하게 다시 진행하고 있다. 하지만 Dockerfile에 이것저것 작성하다보니 따라오는 오류가 계속 생기고 있다. 디버깅은 시간만 있으면 할 수 있을 것 같은데 빌드를 한 번하는 데에 시간이 다소 소요되다보니 고민이 된다. Feedback 주기를 줄이고자 Dockerfile의 설치 패키지를 최소화하는 등 시도를 진행 중이다.

Try
---
1. 