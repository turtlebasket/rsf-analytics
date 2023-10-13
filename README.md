# RSF Analytics

Heatmap of RSF weight room density. Originally made freshman year with [@AlexanderMcDowell](https://github.com/AlexanderMcDowell), and eventually thought I'd turn it into a site.

![](img/demo.png)

## Development (Site)

Install deps:

```
cd site/
poetry install
```

Run dev server:

```
source /path-to-poetry-env/bin/activate
hypercorn main.py -b 127.0.0.1:8000 --reload
```
