# System Architecture

```text
               UNDERGROUND MINE

        +-------------------------+
        | SMART MINER HELMET     |
        | MPU6050 / SOS / OLED   |
        +------------+------------+
                     |
             worker event/data
                     v
        +-------------------------+
        | COMMUNICATION / RELAY  |
        | zone-level last-known  |
        | worker location         |
        +------------+------------+
                     |
                     v
        +-------------------------+
        | SURFACE CONTROL STATION|
        | Flask + Risk Engine     |
        | Dashboard + Alerts      |
        +-------+----------+------+
                |          |
                |          +------------------+
                v                             v
      +------------------+          +-------------------+
      | RESCUE ROVER     |          | HUMAN RESCUE TEAM |
      | camera + sensors |          | informed decision |
      +------------------+          +-------------------+
```

## Prototype boundaries

The current repository demonstrates the integration and emergency workflow. The zone-level location model and demo thresholds are prototypes and must not be treated as mine-safety-certified behavior.
