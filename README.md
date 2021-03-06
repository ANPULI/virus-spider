# virus-spider

This is the backend API for the visualization of the [2019-nCov](https://www.wikiwand.com/en/Novel_coronavirus_(2019-nCoV) "2019 novel coronavirus") in China. The frontend can be found [here](https://github.com/ANPULI/virus-vis).

## Current Progress

- [x] Province-level fata of confirmed/fead/cured cases (2020/1/29)
- [ ] City-level data of confirmed cases
- [x] Nation-level daily data for line charts

## Data Structures

## Total Data

```json
"确诊": {
    "2020年1月11日": [{"name": "湖北省", "value": 41}, {"name": "广东省", "value": 0}, ..., {"name": "全国", "value": 41}],
    ...,
    "累计": [{"name": "湖北省", "value": 4586}, {"name": "广东省", "value": 311,}, ... {"name": "全国", "value": 7209}]
},
"死亡": {
    same as above
},
"治愈": {
    same as above
}
```

## Daily Data

```json
"每日": {
    "日期": ["2020年1月11日", "2020年1月12日", ..., TBD],
    "确诊": [41, 0, ..., TBD],
    "死亡": [1, 0, ..., TBD],
    "治愈": [2, 4, ..., TBD]
}
```

## City-Level Data