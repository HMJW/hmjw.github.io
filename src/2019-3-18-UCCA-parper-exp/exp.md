| description               | dev primary | dev remote | dev average | test wiki primary | test wiki remote | test wiki average | test 20K    primary | test 20K remote | test 20K average |
| ------------------------- | ----------- | ---------- | ----------- | ----------------- | ---------------- | ----------------- | ------------------- | --------------- | ---------------- |
| english-topdown-lstm      | 79.5        | 43.8       | **79.0**    | 77.6              | 48.0             | **77.2**          | 73.3                | 19.0            | **72.3**         |
| english-chart-lstm        | 79.4        | 46.9       | 78.9        | 77.4              | 50.2             | 76.9              | 73.0                | 21.1            | 71.9             |
| english-topdown-attention | 79.0        | 47.5       | 78.5        | 77.5              | 52.4             | 77.0              | 72.6                | 24.4            | 71.5             |
| english-chart-attention   | 79.2        | 48.9       | 78.6        | 77.6              | 50.3             | 77.1              | 73.0                | 28.8            | 72.0             |



由于topdown-lstm最好，以下都用topdown-lstm作为ucca的基础模型。

| description                    | dev primary | dev remote | dev average | test wiki primary | test wiki remote | test wiki average | test 20K    primary | test 20K remote | test 20K primary |
| ------------------------------ | ----------- | ---------- | ----------- | ----------------- | ---------------- | ----------------- | ------------------- | --------------- | ---------------- |
| english-topdown-lstm(baseline) | 79.5        | 43.8       | 79.0        | 77.6              | 48.0             | 77.2              | 73.3                | 19.0            | 72.3             |
| + dep label                    | 80.2        | 49.8       | 79.7        | 78.6              | 53.9             | 78.1              | 74.4                | 28.4            | 73.4             |
| + treegru                      | 80.4        | 52.4       | 79.9        | 78.9              | 54.4             | 78.5              | 75.0                | 30.5            | 74.0             |
| + biaffine lstm feature        | 80.5        | 49.9       | 80.0        | 78.7              | 50.4             | 78.3              | 75.0                | 24.0            | 73.9             |
| MTL                            | 80.9        | 54.4       | **80.4**    | 79.2              | 58.8             | **78.8**          | 75.1                | 32.4            | **74.2**         |



ucca加入bert后。(单语言的，结果比评测时略高)

| description                         | dev primary | dev remote | dev average | test wiki primary | test wiki remote | test wiki average | test 20K    primary | test 20K remote | test 20K primary |
| ----------------------------------- | ----------- | ---------- | ----------- | ----------------- | ---------------- | ----------------- | ------------------- | --------------- | ---------------- |
| english-topdown-lstm+bert(baseline) | 83.0        | 57.4       | 82.6        | 81.6              | 59.3             | 81.2              | 78.2                | 35.5            | 77.2             |
| + dep label                         | 83.1        | 54.0       | 82.6        | 82.1              | 56.7             | **81.7**          | 78.7                | 31.4            | 77.6             |
| + treegru                           | 83.1        | 59.5       | **82.6**    | 81.9              | 59.2             | 81.5              | 78.5                | 44.1            | **77.7**         |
| + biaffine lstm feature             | 83.1        | 58.2       | 82.6        | 81.7              | 58.0             | 81.3              | 78.4                | 38.6            | 77.5             |
| MTL(两边都加了bert)                 | 82.9        | 51.8       | 82.4        | 81.8              | 57.1             | 81.3              | 78.4                | 35.8            | 77.5             |



