# 📊 StatQL

**StatQL** is a desktop‑first SQL engine that streams **fast, *approximate* answers** from your data sources—*without spinning up a server*.

*Initial release ships with connectors for **PostgreSQL**, **Redis** (α quality) and the local **Filesystem**.  More catalogs—cloud object storage, OLAP warehouses, REST APIs—are on the roadmap.*

---

## Quick start

To launch StatQL, install it and start up the local server:

```bash
pip install statql
python -m statql            # launches the Streamlit server
```

Then in your browser, navigate to http://localhost:8501

Integrate your data sources in the `Integrations` page, then start running your queries!

---

## Usage examples

> StatQL emits a fresh result table every 0.5 – 1 s.  Each numeric cell is formatted as `value ± error`, where *error* is the absolute 95 % confidence‑interval half‑width.  As more of the population is sampled, the estimates tighten.

### 1️⃣ Row count per order status (single table)
```sql
SELECT l_linestatus, COUNT() AS rows
FROM pg.local.tpch.public.lineitem
GROUP BY l_linestatus;
```
| l_linestatus | rows |
|--------------|---------------------|
| F | 3 172 481 ± 46 892.7 |
| O | 3 181 633 ± 46 744.2 |

### 2️⃣ Total PNG footprint in `/data/images` (filesystem)
```sql
SELECT divide(SUM(size), 1_073_741_824) AS gib
FROM fs.media_fs.entries
WHERE get_file_ext(path) = 'png';
```
| gib |
|-----------|
| 118.6 ± 5.3 |

### 3️⃣ Row counts across *all* databases in a cluster (wildcards)
```sql
SELECT @db, COUNT() AS rows
FROM pg.us-cluster-4.?.public.lineitem
GROUP BY @db
ORDER BY rows DESC;
```
| @db | rows |
|------|-----------------|
| sales | 12 945 002 ± 99 811.4 |
| hr    |  6 088 551 ± 74 225.9 |
| …     | … |

---

## Video Tutorial

[![StatQL Tutorial](https://img.youtube.com/vi/krLfuwjDv4A/0.jpg)](https://youtu.be/krLfuwjDv4A)

👉 [**Full docs → docs/index.md**](docs/index.md)