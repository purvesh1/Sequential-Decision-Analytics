# Formulating the SDA proble for Trucking Industry

Here’s a refined formulation of the **load booking problem** in truckload dispatching as a **sequential decision problem**, based on the Powell 2007 chapter:

---

## 1. Problem Overview

* **Agents:** A trucking carrier operating a fleet of $N$ trucks.
* **Events:** Customer calls requesting to move loads (from Origin $O$ to Destination $D$), arriving dynamically over time.
* **Decisions:** When each load arrives, decide whether to accept or reject, and if accepted, assign it to a specific truck—or let a truck operate empty until its next load.

The goal is to **maximize long-run profit** considering:

* Revenue from accepted loads;
* Fuel, driving, and deadhead costs;
* Opportunity cost of leaving trucks idle;
* Matching constraints (e.g., driver availability, legal load limits).

---

## 2. State Variables $S_t$

At decision epoch $t$, define state:

* $x_t^i$ = location (and possibly status) of truck $i$, for $i = 1, …, N$;
* Available load backlog (pending load requests);
* Time-of-day, day-of-week — important for travel times/demand patterns;
* Exogenous stochastic elements (e.g., traffic, delays).

So,

$$
S_t = \{(x_t^1, \dots, x_t^N), \text{backlog}_t, t\}
$$

---

## 3. Decision Variables $a_t$

At each arrival, choose:

* **Reject** the load (do nothing);
* **Accept**, and:

  * Determine which truck $i$ to dispatch,
  * Optionally schedule repositioning or “empty miles” if no truck is co-located.

Thus:

$$
a_t \in \{ (\text{accept}, i), \text{reject} \}
$$

---

## 4. Transition Function

Once $a_t$ is made, the state evolves:

* If accept: truck $i$ transitions to the load’s destination over a random travel time; revenue $R(O,D)$ is credited, costs $C_{\text{drive}} + C_{\text{deadhead}}$ are incurred.
* If reject: state remains, truck availability unchanged.
* Loads expire if not served within a time window; new loads arrive randomly.

$$
S_{t+1} = f(S_t, a_t, \omega_t)
$$

where $\omega_t$ represents random elements like load arrivals and travel durations.

---

## 5. Objective Function

Maximize total *expected discounted reward* (or average-per-period):

$$
\max_{\pi} \mathbb{E}^{\pi} \left[ \sum_{t=0}^\infty \gamma^t R(s_t, a_t) \right]
$$

where

$$
R(s_t, a_t) =
\begin{cases}
\text{Revenue}(O,D) - \text{costs}, & \text{if accepting load} \\
0, & \text{if rejecting}
\end{cases}
$$

---

## 6. Sequential Nature & Challenges

* Decisions affect future available location of trucks;
* Problem scale grows rapidly with fleet size and state space;
* Must account for uncertainties in arrivals and travel times;
* Requires trade-off: accept now vs. stay idle for potentially better future loads.

---

## 7. Solution Approaches

### a) Exact Dynamic Programming

Theoretically possible for small fleets or discretized states. Not practical at scale due to the "curse of dimensionality."

### b) **Approximate Dynamic Programming (ADP)**

Powell advocates approximating the **value function** via:

* **Lookahead models** (model predictive control);
* **Single-cut or rollout techniques:** approximate the value of future state for each action;
* **Value function approximation:** regress future values based on state features (e.g., truck distribution across regions).

### c) Heuristics & Dispatching Policies

Common rules include:

* Geographically nearest truck assignment,
* Balancing future opportunities via geographic “reserve” regions,
* Repositioning empty trucks based on forecast demand.

ADP helps to derive improved policies such as **“density-based dispatch”**: base decisions on marginal value of having a truck available in different zones.

---

## 8. Formalization Summary

| Element          | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| **State** $S_t$  | Truck statuses (location/time), current load backlog, time stamp         |
| **Action** $a_t$ | Accept load + assign truck $i$, or reject                                |
| **Transition**   | Trucks move to pick-up and deliver; new loads arrive; backlogs evolve    |
| **Reward**       | $R(S_t,a_t) = \text{Rev}(O,D) - \text{Cost}(O,D,i)$ (zero on rejection)  |
| **Policy** $\pi$ | Mapping $S_t \to a_t$ to maximize expected discounted cumulative rewards |

---

## 9. Extensions & Refinements

* **Multi-period lookahead**: anticipate future load distributions;
* **Rolling horizon control**: re-optimize at each load arrival time shift;
* **Stochastic travel times**: incorporate uncertainty into the transition function;
* **Driver constraints**: include legal hours-of-service and required rests in state variables;
* **Fleet heterogeneity**: different truck types or capacities included.

---

## 10. Next Steps

To implement this:

1. **Define** state representation (e.g., spatial discretization).
2. **Model** load arrival processes and revenue/cost structures.
3. **Implement** ADP via simulation:

   * Use sample paths to learn value estimates,
   * Use features like "trucks in region $r$" and “time to deadline”.
4. **Benchmark** simple heuristics (nearest truck, random assign) vs. improved ADP policies.

---

This formulation aligns with Powell’s approach—model the real-time load assignment as a **stochastic dynamic program**, then apply **ADP** to approximate the value of truck-time and inform dispatch decisions. If you'd like, I can help design the simulation, specify features for value approximation, or outline efficient heuristics.


## References
1. https://castle.princeton.edu/Papers/Powell%20CRC%20chapter%20-%20TL%20dispatching%20Sept%2028%202007.pdf
