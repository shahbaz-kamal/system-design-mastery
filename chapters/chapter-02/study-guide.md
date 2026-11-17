---
title: "Defining Nonfunctional Requirements"
subtitle: "DDIA Second Edition - Chapter 2 - Learning and Interview Handbook"
author: "Source-grounded study edition"
---

# How to use this handbook

Read each lesson before its questions. Trace the diagrams aloud: name the caller, the state being changed, and what happens if the next step fails. Then answer without looking and compare your reasoning with the model answer. Questions marked *Interview* are intended for spoken practice; the others develop the same underlying skills.

This handbook contains **30 main questions, including 12 interview questions, and 30 answered follow-ups**. Printed page references refer to the supplied DDIA second edition, not PDF viewer numbering. Examples labeled supplementary are original teaching examples; their numerical targets are illustrative, not production recommendations. Course references use physical slide numbers in the supplied PPTX files.

# Section 1 - Requirements and the timeline case study

*Source: [DDIA Ch.2, introduction and Case Study: Social Network Home Timelines, printed pp. 33-36].*

## Learning outcomes and prerequisites

Distinguish a feature from the conditions under which it must work; explain fan-out and the read/write trade-off in materialized timelines.

**Functional requirement:** the behavior a product offers, such as publishing a post. **Nonfunctional requirement:** a quality or constraint on that behavior, such as delivering posts promptly under a specified load. **Derived data:** information computed from another authoritative representation. **Materialized view:** a stored query result maintained as its inputs change. **Fan-out:** one operation producing many downstream operations.

## Lesson - A correct feature can still be unusable

A social network may implement posting and following correctly while making its home timeline painfully slow. The feature exists, but the system does not meet the conditions users need. Nonfunctional requirements make those conditions explicit. Performance, reliability, scalability, and maintainability interact: a fast cache adds maintenance work, and replicating it adds failure cases. Security is also a nonfunctional concern, but a full security treatment is outside this chapter.

Start with three relational entities: users, posts, and follow relationships. A timeline read finds the accounts followed by the viewer, fetches their recent posts, merges them by time, and returns a bounded result. This is an understandable baseline. Its difficulty is repeated work: many viewers repeatedly fetch overlapping sets of posts. Polling also sends requests when nothing has changed.

The book uses approximately 500 million posts per day, about 5,800 per second on average, and a much higher possible peak. With 10 million online clients polling every five seconds, there are two million timeline requests per second. At 200 followed accounts per viewer, the simplified estimate becomes 400 million per-account lookups per second. These are workload illustrations, not a benchmark of a real database or a claim that each logical lookup must require a separate network request.

Materialization moves much of that work to the write path. The application stores a new post, finds its followers, and adds a reference to each follower's precomputed timeline. Reading then becomes a bounded lookup in the timeline store. A subscription can push updates to an online client instead of having it repeatedly poll. Materialization and push delivery solve different problems: one avoids repeated query computation; the other avoids repeatedly asking whether something changed.

This exchange creates write amplification. At 5,800 posts per second and a simplified fan-out of 200, maintenance requires about 1.16 million timeline insertions per second. A queue can absorb a temporary spike, but it does not remove the work. When input exceeds processing capacity for long enough, backlog and freshness delay grow. The useful measurement is therefore not just timeline read time, but also post-to-timeline delivery delay.

Follower counts are highly uneven. Treating a celebrity like an ordinary author can require millions of timeline updates for one post. A hybrid design keeps ordinary authors on the materialized path and merges celebrity posts at read time. This reduces extreme write work while making reads more complicated. Similarly, an unusually active viewer's derived timeline may be sampled if product requirements allow it; that permission is a product decision, not an automatic performance optimization.

## Worked example - Follow the state

[Supplementary example] A Node.js API accepts a post and stores it in PostgreSQL. A durable job records that follower timelines need updating; a worker updates a Redis-derived timeline with bounded recent post IDs. The exact handoff must prevent a committed post from being silently omitted after a crash. A transactional outbox is one possible implementation, introduced here as an extension rather than a mechanism explained by this chapter. Redis is a derived view in this example; the durable post remains in PostgreSQL.

![Original timeline materialization flow](diagrams/output/chapter-02/timeline.png)

The solid path creates durable state and schedules work. The worker-to-timeline arrow is repeated across followers. The read path fetches the derived result and combines exceptional authors where required. A cache failure should trigger a controlled fallback or rebuild; allowing all clients to run expensive reconstruction queries simultaneously can overload the database.

## Remember this

- Define both visible behavior and the conditions under which it must work.
- Materialization exchanges repeated read work for maintained derived state.
- A queue absorbs bursts; sustained excess input still needs a capacity or workload change.
- Averages hide the celebrity cases that dominate fan-out.


## Practice and interview questions

### Q01. What distinguishes functional and nonfunctional requirements?

**Model answer:** Posting an order is functional behavior. Serving it correctly within an agreed response-time distribution under a defined workload is a nonfunctional requirement. Connect the quality to a user journey instead of merely saying the system must be fast. Record load, resources, and acceptable outcomes because performance, reliability, and maintenance effort can conflict.

**Follow-up:** Can a correct feature still fail its purpose?

**Follow-up answer:** Yes. A correct timeline delivered too late to be useful fails its timing requirement. Evaluate the delivered experience as well as the business calculation.

### Q02. Interview — How would you design a social-network timeline?

**Model answer:** Start with users, posts, and follows and a read-time merge of followed accounts. Establish load and freshness before optimizing. When repeated reads dominate, precompute timelines and maintain them on writes. Retain authoritative posts for repair. Treat high-follower authors separately when their fan-out dominates. Compare read cost, update cost, and delivery delay rather than presenting a cache as the complete design.

**Follow-up:** Why treat celebrities separately?

**Follow-up answer:** One post can require millions of updates. Keeping exceptional posts separately and merging them on read reduces write amplification while adding read logic and another freshness path.

### Q03. How does materialization change work?

**Model answer:** It stores a query result and maintains it when inputs change. Viewers avoid repeatedly gathering and sorting the same posts. Saved read computation becomes update work, storage, and recovery responsibility. Define acceptable staleness and how a damaged derived view is rebuilt. Materialization is valuable when that exchange fits the workload, not simply because reads can become faster.

**Follow-up:** Does push delivery replace materialization?

**Follow-up answer:** No. Push determines how updates reach a client; materialization determines how a result is computed and stored. Either can exist without the other.

### Q04. Interview — What happens when timeline traffic spikes?

**Model answer:** Separate read-serving from update processing. A durable queue smooths a temporary burst while cached timelines stay cheap to read, but freshness degrades as backlog grows. Measure oldest job age and post-to-timeline delay. Bound backlog and define behavior when freshness objectives cannot be met. Protect ordinary work from exceptional fan-out rather than letting one author monopolize workers.

**Follow-up:** What if demand stays above worker capacity?

**Follow-up answer:** Backlog keeps growing unless demand falls or efficiency or capacity improves. A larger queue delays exhaustion but does not fix the sustained imbalance.

### Q05. Why are average follower counts insufficient?

**Model answer:** Fan-out depends on the distribution. A few enormous audiences create concentrated bursts; some viewers also follow unusually many active accounts. Measure extreme cases and their frequency. Use exceptional handling only when workload evidence and product semantics justify it. The average alone cannot tell you which requests dominate resource needs or delivery delay.

**Follow-up:** May updates be dropped to control cost?

**Follow-up answer:** Only when the product permits sampling for that population. Silently dropping required updates changes correctness. The book distinguishes sampling an overloaded viewer's feed from indiscriminately omitting celebrity delivery.

# Section 2 — Describing Performance

*Source: [DDIA Ch.2, Describing Performance and Latency and Response Time, printed pp. 37–39]; [Course Lecture 2, inspected slides 6, 14–21, 27–34].*

## Learning outcomes and prerequisites

Distinguish response time from throughput, locate waiting, and explain overload feedback.

**Throughput** is completed work per unit time. **Response time** is elapsed time at the caller. **Service time** is active processing time. **Queueing delay** is waiting for an available resource. **Head-of-line blocking** means earlier work delays later work. **Backpressure** asks upstream producers to slow down.

## Lesson — Find where a request spends time

A service completing more requests per second is not necessarily giving each user a faster response. Throughput describes the rate of work; response time describes an individual operation. Both depend on the workload and resources. Small cached reads and large uploads are different workloads even if their request rates match.

Trace an order-status request from a browser through a Node.js application to PostgreSQL. It crosses a network, waits for application processing, waits for a connection, executes a query, and returns. The application may actively process it for only a small portion of the total. A SQL timer therefore cannot explain all client-visible delay. A server request timer also excludes some client and network intervals. State the measurement boundary before comparing numbers.

DDIA uses latency for time during which a request is latent rather than actively processed; network latency is one example. The performance lecture sometimes uses latency more broadly for request-response time. This handbook names client-observed response time explicitly. Two dashboards can disagree because they correctly measure different intervals.

At light load, new requests can begin promptly. Near capacity, they wait behind existing work. A few slow operations occupying scarce connections or execution slots can delay later operations with short service times. Increasing a queue's limit creates room for waiting, not processing capacity. A large queue can turn early rejection into late failure.

Now add retries. A caller times out and sends another attempt while the original is still executing. More work produces longer queues, causing more timeouts and retries. This feedback can leave the system overloaded even after external demand falls: the book calls this a metastable failure. Recovery may require reducing admission, safely removing expired work, or resetting affected resources.

The lecture's queue model is a useful diagnostic aid, but not every delay is a queue. Network propagation and inherently long computations also take time. Locate contention with measurements rather than treating a slogan as a physical law. Compare response distributions, errors, arrival rate, connection waits, queue age, and resource pressure.

## Worked example — Bound the work

[Supplementary example] A service sustainably handles 1,000 operations per second for a defined request mix. A 1,300-per-second burst adds approximately 300 queued operations each second in a simplified constant-rate model. A 3,000-item buffer buys around ten seconds before filling. It does not create sustainable capacity for 1,300 operations per second.

Use bounded admission, deadlines, and selective retries with exponential backoff and jitter. Backoff reduces attempt frequency; jitter spreads attempts in time. A circuit breaker temporarily restricts calls to a failing dependency. Load shedding rejects work that cannot safely be handled. Each needs explicit user-visible behavior: silently losing an accepted order is not a valid overload policy.

![Response-time components and retry feedback](diagrams/output/chapter-02/response.png)

## Remember this

- Response time includes waiting; service time can look healthy during an incident.
- Throughput capacity depends on the request mix and available resources.
- Retries consume capacity and may create positive feedback.
- Bound work and make overload behavior observable.


## Practice and interview questions

### Q06. Interview — How do response time and throughput differ?

**Model answer:** Response time is elapsed time for one request at a specified boundary. Throughput is completed operations or data volume per time unit. More concurrency may raise throughput while individual requests become slower because of waiting. Report workload, resources, errors, and duration percentiles together. A single requests-per-second number cannot establish that the user experience improved.

**Follow-up:** Is 10,000 requests per second always better than 5,000?

**Follow-up answer:** No. Operations may differ in size or complexity, or the higher rate may violate timing and correctness objectives. Compare equivalent work and useful outcomes.

### Q07. Where can a request wait?

**Model answer:** It can wait in a network buffer, execution queue, database connection pool, lock queue, or downstream dependency. The caller sees those waits plus active processing and transit. Instrument intervals to locate the dominant component. A fast SQL timer cannot establish a fast end-to-end journey because much of the delay may occur before the query begins.

**Follow-up:** What is head-of-line blocking?

**Follow-up answer:** Earlier slow operations occupy a constrained resource and delay later work that could otherwise finish quickly. Short processing time does not prevent a long total response time.

### Q08. Interview — Why can low CPU coexist with slow responses?

**Model answer:** The constraint may be a connection pool, lock, disk, network, or remote service. CPU reports one resource and may average across cores or hosts. Trace slow operations and inspect waits and dependency behavior before adding capacity. The correct intervention depends on what prevents work from progressing, not whichever metric happens to be easiest to graph.

**Follow-up:** Would more application instances necessarily help?

**Follow-up answer:** No. They may increase pressure on a constrained database. Add instances when application capacity is the measured limit and downstream resources can support the extra work.

### Q09. How can retries cause an outage?

**Model answer:** An original operation can continue after its caller times out. A retry adds work, increasing queues and producing more timeouts and attempts. This feedback can persist after external traffic falls. Bound attempts, propagate deadlines, use exponential backoff and jitter, and protect admission. Retrying must also preserve business correctness when the first attempt may already have succeeded.

**Follow-up:** What does a circuit breaker add?

**Follow-up answer:** It temporarily restricts calls after recent failures instead of continually trying. Recovery probes should be bounded so callers do not all resume full traffic simultaneously.

### Q10. What does a bounded queue achieve?

**Model answer:** It limits memory use and waiting work and provides an explicit point to reject or slow producers. Choose its size in relation to processing rate and acceptable delay. A queue helps with short bursts, but can conceal sustained overload or hold requests that have already expired. Observe queue age as well as item count.

**Follow-up:** Is a larger queue safer?

**Follow-up answer:** It may absorb a larger burst, but also increases waiting and recovery time. It does not increase sustainable processing throughput.

# Section 3 — Distributions and Service Objectives

*Source: [DDIA Ch.2, Average, Median, and Percentiles; Use of Response Time Metrics, printed pp. 40–42]; [Course Lecture 2, inspected slides 28–34].*

## Learning outcomes and prerequisites

Interpret percentiles, explain tail amplification, and define a measurable performance objective.

**Mean** is sum divided by count. **Median/p50** describes the midpoint of sorted observations. **p99** is a threshold around which 99% of observations lie at or below it, subject to estimator and ties. **Tail latency** concerns slow outliers. An **SLO** is a service level objective; an **SLA** specifies contractual consequences for missed promises. A **histogram** counts observations in ranges.

## Lesson — One number hides different experiences

Request durations vary because of garbage collection, contention, retransmission, disk access, and other effects. A mean summarizes all observations but cannot tell you which fraction is suffering. The median describes the middle; high percentiles expose progressively smaller slow portions. Neither a low mean nor a low median establishes an acceptable tail.

Imagine 100 requests: 95 take 100 ms and five take 2,100 ms. Their mean is 200 ms, median is 100 ms, and nearest-rank p99 is 2,100 ms. Reporting only the mean suggests an experience none of these requests had. High percentiles from small samples are unstable; different percentile estimators may also give different exact values. Record sample sizes and calculation methods when comparing results.

Tail behavior matters when one request requires many calls. A page that needs all twenty parallel backend results waits for the slowest. If calls independently have a 1% chance of exceeding a threshold, the chance that at least one does is 1 − 0.99^20, about 18.2%. Real calls can share dependencies and be correlated, so that formula is an illustration rather than a production prediction. Parallelism reduces serial waiting but does not eliminate the slowest required branch.

An SLO makes user needs testable. State the operation, counted population, measurement point, window, and target. The book illustrates median and p99 targets alongside successful-request objectives. An SLA adds agreed consequences such as refunds. It is not merely another name for a graph. Keep errors visible: returning immediate failures must not make a dashboard claim that user experience improved.

The book also warns about repeating simplistic claims that a fixed speed improvement produces a fixed revenue increase. A fast error page and a slower useful page differ in content, not just speed. Correlation does not establish causation. Compare equivalent journeys and control meaningful confounders before using such evidence to justify investment.

## Worked example — Combine distributions

[Supplementary example] Propose a checkout objective: over a 30-day window, at least 99.9% of valid checkout requests succeed and p99 response time is below one second at the agreed boundary. These are illustrative targets, not universal recommendations. Decide how rejected requests are counted before measuring compliance.

Instances record compatible histogram buckets. The monitoring system combines bucket counts and estimates p99 from the combined distribution. Averaging instance p99 values is invalid, even if weighted by traffic: percentile values have already discarded the distribution information needed for correct aggregation. Preserve the observations, compatible histogram counts, or a supported mergeable sketch.

## Remember this

- Read median and tail percentiles with volume and error rate.
- Parallel fan-out can amplify tail exposure.
- Merge compatible distributions before computing fleet percentiles.
- Define population, boundary, window, and outcome in an SLO.


## Practice and interview questions

### Q11. How do mean, median, and p99 differ?

**Model answer:** The mean combines durations arithmetically. The median describes the midpoint of sorted observations. p99 describes a slow threshold around the upper one percent, subject to ties and estimator. Use them together rather than treating any one as the complete experience. Report sufficient observations for very high percentiles and avoid presenting p99 as the maximum.

**Follow-up:** Is the mean ever useful?

**Follow-up answer:** Yes. It summarizes accumulated time per observation and can support capacity reasoning under appropriate assumptions. Its weakness is being used as a complete description of the distribution.

### Q12. Interview — How would you define a performance SLO?

**Model answer:** Name the operation, counted requests, measurement point, time window, and target. Propose a checkout percentile threshold and successful-request objective, then validate the targets against user needs and cost. These are design choices rather than universal values. Keep errors visible so replacing useful responses with immediate failures cannot masquerade as improved performance.

**Follow-up:** How is an SLA different?

**Follow-up answer:** An SLA specifies agreed consequences for missing service promises. An internal SLO can guide engineering without itself being a customer contract.

### Q13. Why do parallel backend calls amplify tail latency?

**Model answer:** When the caller requires every result, completion depends on the slowest branch. More branches provide more chances to encounter an outlier. Under independent 1% slow-call probabilities, twenty calls have approximately an 18.2% chance of at least one slow result. Shared dependencies can violate independence, changing the calculation without removing the underlying exposure.

**Follow-up:** Should every call become optional?

**Follow-up answer:** No. Distinguish required outcomes from optional enhancements. Recommendations may degrade gracefully; required payment confirmation cannot simply be omitted while claiming success.

### Q14. Interview — How do you calculate fleet p99 correctly?

**Model answer:** Combine compatible observations, histogram counts, or supported mergeable sketches and compute p99 from that combined distribution. Do not average instance p99 values. Preserve the population and time window, and check estimator accuracy and sample volume. A fleet metric must reflect actual request counts rather than treating a nearly idle instance like a heavily loaded one.

**Follow-up:** Does weighting individual p99 values fix aggregation?

**Follow-up answer:** No. Percentiles discard distribution information. Weighting the thresholds cannot reconstruct the missing observations; merge the distribution data instead.

### Q15. How should speed and conversion claims be evaluated?

**Model answer:** Check whether comparisons control page usefulness, errors, user population, and other changes. A fast empty page and a slower useful page differ in more than speed. The book cautions against universal revenue claims based on weak comparisons. Measure equivalent journeys and investigate confounders before treating a correlation as evidence of a causal business benefit.

**Follow-up:** Why might a faster page convert worse?

**Follow-up answer:** It might be an error page or lack useful content. That observation does not establish that speeding up an otherwise equivalent useful page harms conversion.

# Section 4 — Reliability and Fault Tolerance

*Source: [DDIA Ch.2, Reliability and Fault Tolerance and its subsections, printed pp. 43–49]; [Course Lecture 5, inspected slides 7–14, 22–24, 30, 34–44].*

## Learning outcomes and prerequisites

Define a fault model, explain correlated failures, and design recovery around technical and human realities.

A **fault** is a part not working correctly; a **failure** is the system missing its required service. **Fault tolerance** preserves service despite specified faults. A **single point of failure** can escalate its fault into service failure. A **failure domain** groups resources exposed to a shared cause. **Idempotency** means repetition preserves the intended single-operation effect.

## Lesson — Preserve the promise when a component breaks

Reliability means continuing to work correctly when things go wrong. Correctness includes more than reachability: a service returning the wrong balance quickly is unreliable. Fault and failure depend on the boundary. A disk can fail while the larger service tolerates that event through other copies and continues serving users.

Fault tolerance has limits. State the faults and number assumed: losing an application instance differs from losing an availability zone. Copies sharing a machine, rack, deployment, or control plane share risks. Surviving resources need sufficient capacity and correct recovery behavior. Redundancy is a mechanism, not a proof of availability.

### Hardware and Software Faults

Hardware can stop working or silently corrupt results. At large scale, individual faults become routine. Distribution can permit maintenance and tolerate machine or location loss. But replication does not replace recoverable backups: accidental deletion may propagate to every live replica.

Software faults are often strongly correlated because nodes run the same code. A bad deployment can break every copy; a shared dependency can hang; a runaway process can exhaust resources. Isolation, bounded work, staged releases, assumption testing, and production monitoring reduce different risks. Adding replicas of the same bug does not fix the bug.

Consider a timeline worker crashing after updating half its followers. Recovery needs durable work and a safe way to resume. A uniqueness rule on (viewer_id, post_id) can prevent duplicate derived entries when work repeats. This is deduplication of effects; it does not imply the network delivers each message exactly once. Durable handoff, progress tracking, and safe repeated effects are distinct responsibilities.

The course frames fault handling as redundancy, detection, and recovery. A spare is useless if traffic never reaches it after failure. Health checks must test enough to detect useful service while avoiding shared false alarms that remove every node at once. A timeout indicates the caller did not receive a timely result; the remote operation may still have committed.

### Humans and Reliability

Operators act with incomplete information and competing demands. Blaming the final person who deployed misses the conditions that made damage easy and recovery hard. Safe defaults, clear interfaces, gradual rollout, monitoring, and rollback reduce consequences. Blameless postmortems reconstruct what people knew and produce concrete improvements to the technical and organizational system.

Fault injection deliberately exercises recovery paths instead of assuming dormant failover works. Define a bounded experiment, expected outcome, and stop conditions. Verify business results as well as process restarts. Reliability investment should reflect harm: permanent loss and corruption can matter much more than a brief outage.

## Worked example — Retry after an uncertain outcome

[Supplementary example] A checkout caller submits a unique request key. The server stores the key and durable order result atomically. If the reply disappears, the same key can return the previous outcome. A payment provider needs its own compatible identity and reconciliation; a local database transaction cannot atomically control an unrelated remote service. Test the crash after commit but before reply and verify one business effect.

![Failure detection and controlled recovery](diagrams/output/chapter-02/recovery.png)

## Remember this

- State the tolerated fault model and system boundary.
- Redundancy needs detection, correct recovery, and surviving capacity.
- A timeout does not prove non-execution.
- Improve working conditions and defenses after incidents.


## Practice and interview questions

### Q16. Interview — Distinguish fault, failure, and fault tolerance.

**Model answer:** A fault is a part not operating correctly; a failure is the system missing its required service. Fault tolerance prevents specified component faults from becoming service failure. State the boundary and assumptions: a disk can fail while the larger replicated service keeps operating correctly. The same event receives different descriptions at different levels without contradiction.

**Follow-up:** Can a system tolerate every fault?

**Follow-up answer:** No. Tolerance is bounded by fault type, number, and surviving resources. A claim without those limits is incomplete.

### Q17. Why is replication insufficient for reliability?

**Model answer:** Copies can share power, deployment bugs, overload, credentials, and destructive updates. Survivors need adequate capacity, correct state, detection, and working takeover logic. Replication improves availability for particular faults but does not replace recoverable backups or safe deployment. Evaluate the complete path, including dependencies that might remain single points of failure.

**Follow-up:** Why separate failure domains?

**Follow-up answer:** Resources sharing a rack or location can fail together. Separation reduces those correlated risks, although shared software and control planes can still affect all copies.

### Q18. Interview — How do you retry a timed-out order safely?

**Model answer:** Treat the result as unknown. Store an operation identity atomically with the durable result and return that result on retry. Use durable uniqueness to prevent concurrent duplicates. External effects need compatible identity and reconciliation because a local transaction cannot control a remote provider. Verify the crash-after-commit case instead of testing only clean success and early rejection.

**Follow-up:** Does timeout prove rejection?

**Follow-up answer:** No. The operation may have committed before the reply was lost. Creating a new operation without checking identity can duplicate its business effect.

### Q19. What should fault injection verify?

**Model answer:** Choose a specific fault, affected boundary, expected outcome, and bounded experiment. Remove an instance or kill a worker and observe recovery, business effects, delays, and backlog. Define stop conditions and monitor the remaining capacity. A restart alone proves little if accepted work is lost, duplicated, or delayed beyond the required objective.

**Follow-up:** What if checks pass but data is wrong?

**Follow-up answer:** The experiment failed its correctness goal. Validate durable outcomes and business invariants as well as process health and request error rates.

### Q20. How does a blameless postmortem help?

**Model answer:** Reconstruct decisions using the information available at the time and identify technical and organizational conditions. Produce concrete improvements to interfaces, rollout, diagnostics, training, or investment. Blame discourages the detailed reporting needed to uncover interactions and recurring hazards. The goal is a safer working system rather than simply a better explanation for the most recent incident.

**Follow-up:** Does blameless mean no accountability?

**Follow-up answer:** No. Teams still own corrective actions and verify completion. Accountability centers on improving conditions and defenses rather than punishing the final actor.

# Section 5 — Scalability

*Source: [DDIA Ch.2, Scalability and its subsections, printed pp. 49–52].*

## Learning outcomes and prerequisites

Describe growth precisely, compare scaling architectures, and choose a response to measured limits.

**Load parameters** describe demand. **Vertical scaling** adds resources to a machine; **horizontal scaling** adds machines. **Shared-memory** threads use common RAM. **Shared-disk** nodes have separate compute and memory but shared storage. **Shared-nothing** nodes own their resources and coordinate through networked software.

## Lesson — Scale a specified workload

Scalability is an ability to cope with a specified increase in load. It is not a universal label attached to a framework. Ask what grows, which outcomes must remain acceptable, and which resources may change. More reads, larger histories, bigger payloads, and more writes can stress very different paths.

### Understanding Load

Record rates, peak concurrency, payload and data sizes, read/write ratios, cache behavior, and skew. Registered accounts are not equivalent to active shoppers. In timelines, follower distribution shapes fan-out; in commerce, a few large customers can dominate query cost. An average user can therefore be a poor planning unit.

Run two kinds of experiment. Hold resources fixed while increasing a load dimension and observe performance; or increase resources to preserve performance as load grows. Linear scalability means doubling relevant resources supports twice the load at equivalent performance over the measured range. It is not a promise that the relationship continues indefinitely. Shared bottlenecks and coordination may make cost grow faster than demand.

### Shared-Memory, Shared-Disk, and Shared-Nothing Architectures

Vertical scaling is often the simplest intervention. More RAM can retain a working set; more cores help only when software and work can exploit them. Threads share memory and require synchronization. Serial work and contention limit gains, while larger machines have price and capacity ceilings. Simplicity can still make them the right choice.

Traditional shared-disk architectures let separate compute nodes access common storage. Contention and coordination can limit scaling. The book distinguishes newer specialized storage-service APIs from older shared filesystem or block-device approaches: superficial similarity does not imply the same limits.

Shared-nothing systems give each node its own compute, memory, and disk. They can scale out and distribute some failure risks, but state must be divided and network behavior handled explicitly. Later chapters explain partitioning and coordination in detail. Adding stateless application servers is only application-tier scaling; it does not automatically distribute the database's workload.

### Principles for Scalability

Break work into largely independent components where useful, while keeping complexity proportional to need. A modular application and one database may be appropriate now. Document its measured limit and a plausible next step instead of implementing every future topology. Revisit assumptions at major growth steps: a design suitable for one order of magnitude can need revision at the next.

## Worked example — Scale the constrained resource

[Supplementary example] An order API grows from 200 to 400 requests per second. If PostgreSQL lock contention dominates, doubling application instances may worsen the bottleneck. Compare connection waits, query durations, lock waits, and I/O under a representative request mix. Improve unnecessary work, then repeat the same objective and workload. Cold-cache behavior must be checked separately because it can sharply increase database demand.

## Remember this

- Specify the growth dimension and performance target.
- Scale the actual bottleneck.
- Distribution adds coordination and recovery responsibilities.
- Preserve flexibility while preparing for evidence-backed growth.


## Practice and interview questions

### Q21. What belongs in a load description?

**Model answer:** Include operation rates, peak concurrency, payload sizes, read/write ratios, dataset size, cache behavior, and skew. Report time variation and distribution where they change cost. These details show which growth dimensions increase work and which objectives will fail first. User count alone does not reveal what the system is doing or how expensive each operation is.

**Follow-up:** Why is registered-user count weak?

**Follow-up answer:** It does not establish active concurrency, request intensity, or per-user data. Systems with equal account counts can have very different capacity requirements.

### Q22. Interview — When would you scale up versus out?

**Model answer:** Choose based on measured constraints, expected growth, cost, and operational needs. Scaling up can simplify a manageable database or memory-bound working set. Scaling out can add capacity and distribute some failures, but state partitioning and coordination add work. Compare these consequences rather than selecting a topology because it is associated with a famous large service.

**Follow-up:** Can more cores fail to help?

**Follow-up answer:** Yes. Serial work, lock contention, I/O limits, or software unable to exploit parallelism can dominate. Measure equivalent workload and outcomes after the change.

### Q23. How do the three sharing architectures differ?

**Model answer:** Shared-memory threads use common RAM. Shared-disk nodes have separate compute and memory but common storage. Shared-nothing nodes own local resources and communicate through networked software. Each moves the location of contention and coordination. New specialized storage-service APIs should not automatically be assumed to inherit every limitation of older shared-disk designs.

**Follow-up:** Does shared nothing mean no communication?

**Follow-up answer:** No. Nodes still exchange requests and coordinate state. The term describes resource ownership, not independence from network and consistency concerns.

### Q24. Interview — How would you test linear scalability?

**Model answer:** Use a representative workload and stable objective. Measure a baseline, then increase resources and demand proportionally while checking duration distribution, errors, correctness, and cost. Account for warmup, skew, and shared bottlenecks. Repeat across the range you intend to claim. One favorable measurement cannot establish that the relationship continues at every future scale.

**Follow-up:** What if throughput doubles but p99 worsens?

**Follow-up answer:** The chosen performance objective has not been preserved. Reporting only completed work conceals the delay paid by slower users.

### Q25. Why avoid scaling too far ahead of need?

**Model answer:** Extra distribution introduces coordination, failure handling, operational burden, and constraints on change. Early product work often benefits more from flexibility than hypothetical capacity. Keep a simple design with measured limits and plausible next steps. Revisit major assumptions when growth provides evidence instead of committing to every possible future topology immediately.

**Follow-up:** Does this mean ignoring future load?

**Follow-up answer:** No. Identify plausible growth and expensive irreversible choices. Preserve options without automatically implementing all of them.

# Section 6 — Maintainability

*Source: [DDIA Ch.2, Maintainability and its subsections; Summary, printed pp. 52–56].*

## Learning outcomes and prerequisites

Connect operability, simplicity, and evolvability to safe operations and change.

**Operability** makes production manageable. **Abstraction** exposes useful operations while hiding mechanisms. **Coupling** describes dependencies between parts. **Evolvability** supports changing needs. **Reversibility** permits safe retreat from a change. **Technical debt** increases the cost of later work.

## Lesson — Design for the people who inherit the system

Initial development is only part of a system's cost. People diagnose incidents, patch dependencies, fix bugs, meet new requirements, and keep production healthy during those changes. Every valuable long-lived system eventually becomes legacy software. Maintainability supports that continued work; it is more than keeping functions short.

### Operability: Making Life Easy for Operations

Operators need meaningful measurements, clear configuration, diagnostic tools, and understandable maintenance procedures. A system that silently retries forever is harder to operate than one exposing stalled work, backlog age, and rejection reasons. Avoiding dependence on one irreplaceable machine also supports planned maintenance.

Automation reduces repetition but can spread mistakes quickly. The manual cases left behind may be especially difficult. Expose automation's actions, bound its reach, and provide documented controls for exceptional cases. Skilled operators and predictable behavior remain necessary even when routine tasks are automatic.

### Simplicity: Managing Complexity

Complexity raises the risk that a local change violates a hidden assumption. Yet line count is not a reliable measure of simplicity. A small interface can hide a complicated implementation, while an excessively generic abstraction can burden every caller. Judge whether engineers can build a correct mental model and perform realistic tasks safely.

The book discusses essential versus accidental complexity while warning that the boundary shifts as tooling changes. SQL hides storage mechanisms and lets many applications use queries without implementing a storage engine. That abstraction does not remove index, transaction, or capacity constraints. A good abstraction reduces routine cognitive burden while leaving relevant limits explainable.

### Evolvability: Making Change Easy

Requirements, platforms, dependencies, and users change. Persistent data often outlives a deployment. Loose coupling helps, but service count alone does not establish flexibility: ten services requiring synchronized releases remain operationally coupled. A modular application can evolve well when its boundaries are clear.

Reversibility reduces the risk of adopting an improvement. A database migration that cannot safely retreat has higher stakes than one retaining a compatible old path. Plan recovery for data as well as binaries. Redeploying old code does not reconstruct information already discarded.

## Worked example — Stage a representation change

[Supplementary example] Renaming a status field used by several application versions requires a compatibility period. Add the new representation, deploy compatible readers and writers, backfill carefully, compare results, and remove the old representation only after consumers migrate. During overlap, define the authoritative value and detect disagreement. This is an example of staged evolution, not a detailed recipe from Chapter 2.

Delay destructive cleanup until the new path is verified and recovery needs are satisfied. The extra temporary work makes the change safer to attempt. That is the practical connection between evolvability, operability, and reliability: people can understand the transition, observe its effects, and recover when expectations are wrong.

## Remember this

- Operability supports people running the service.
- Simplicity means understandable behavior and boundaries.
- Abstractions hide mechanisms without removing constraints.
- Staged, reversible changes improve evolvability.

## Practice and interview questions

### Q26. How do the maintainability principles differ?

**Model answer:** Operability helps people run the service. Simplicity helps them understand it. Evolvability helps them change it safely. They reinforce one another while addressing different work. Clear operational behavior, useful abstractions, and compatible staged changes help maintain the system across staff changes, platform updates, and new requirements rather than only during its first implementation.

**Follow-up:** Is a small codebase always maintainable?

**Follow-up answer:** No. Hidden coupling, undocumented state, and surprising defaults can make a short implementation difficult to operate and change.

### Q27. Interview — What makes a system operationally ready?

**Model answer:** Provide meaningful measurements, diagnostic tools, understandable configuration, maintenance procedures, and predictable recovery controls. Demonstrate instance replacement and detection of stalled work. Expose automated decisions and permit bounded intervention when automation reaches an exceptional case. Readiness is evidence that people can operate the behavior, not simply that deployment succeeded once.

**Follow-up:** Can automation reduce operability?

**Follow-up answer:** Yes. An opaque feedback loop can spread mistakes quickly and be difficult to diagnose. Provide limits, visible actions, and understandable recovery procedures.

### Q28. How does abstraction reduce complexity?

**Model answer:** It exposes operations people need while hiding mechanisms they should not reimplement. SQL lets applications query data without constructing a storage engine. A good abstraction remains understandable and exposes relevant constraints. An excessively generic or leaky interface can instead increase the burden on every caller and make failures harder to reason about.

**Follow-up:** Does abstraction remove underlying costs?

**Follow-up answer:** No. Queries still consume CPU, I/O, and coordination. Hiding mechanisms from routine code does not remove their importance during diagnosis.

### Q29. How does reversibility improve evolvability?

**Model answer:** Safe retreat lowers the risk of changing behavior or data representation. Stage compatible interfaces, retain necessary old data temporarily, compare outcomes, and delay destructive cleanup. Recovery must cover persistent state as well as code. Reverting a binary cannot reconstruct discarded information or automatically undo an incompatible schema transformation.

**Follow-up:** When can old data be removed?

**Follow-up answer:** After consumers migrate, correctness is verified, and agreed recovery needs are met. Removal is a deliberate final step rather than an automatic result of deploying new code.

### Q30. Interview - How would you review a redesign across this chapter?

**Model answer:** Identify which measured requirement it improves, the workload and fault assumptions, how outcomes will be verified, and who will operate and evolve it. Compare simpler alternatives and migration risk. State accepted trade-offs: a faster derived read adds update work, freshness delay, and recovery responsibility. An attractive diagram cannot substitute for these explanations and evidence.

**Follow-up:** What would make you reject the proposal?

**Follow-up answer:** Missing required outcomes, an untested critical recovery path, unjustified operating burden, or unsafe data migration are reasons to reject or revise it before rollout.

# Chapter glossary and concept relationships

**Materialization:** Maintained derived state: saves read computation, adds update work.

**Fan-out:** One input produces multiple downstream operations; skew shapes cost.

**Response time:** Caller-observed elapsed time including waiting and transit.

**Throughput:** Completed work per time unit for a specified workload.

**Tail percentile:** Threshold describing slow observations; not a maximum.

**SLO / SLA:** Measurable objective / agreement defining consequences.

**Fault / failure:** Component malfunction / service missing its promise.

**Failure domain:** Resources exposed to a common cause of failure.

**Idempotency:** Repetition preserves the intended single-operation effect.

**Scalability:** Coping with specified growth while meeting performance needs.

**Operability:** Ease of running, diagnosing, and recovering the service.

**Evolvability:** Ease of adapting behavior and data to new needs.


Performance affects reliability when delay violates the service promise. Scalability protects performance as demand changes. Maintainability supports reliable operations and safe capacity improvements. A materialized view connects all four: fast reads, extra update load, recovery requirements, and a representation that must change with the product.

# Common mistakes

**Saying ?fast? without conditions:** State operation, load, resources, boundary, and objective.

**Averaging instance p99 values:** Merge compatible distributions first.

**Assuming a timeout means no effect:** Treat outcome as unknown; preserve operation identity.

**Assuming copies solve every fault:** Check shared risks, capacity, detection, and recovery.

**Adding servers to any bottleneck:** Locate the constrained resource before scaling.

**Treating automation as understanding:** Expose actions and provide recovery controls.

**Treating code rollback as data recovery:** Plan persistent-state recovery separately.


# Revision exercises and answer key

**A.** One million clients poll every five seconds. What is the request rate? *Answer: 200,000 per second if each sends one request per interval and arrivals are evenly spread. Synchronized polling creates larger peaks.*

**B.** A queue receives 900 items per second and workers finish 800. What grows? *Answer: approximately 100 waiting items per second under constant rates, until demand or capacity changes.*

**C.** Payment commits but its reply is lost. What must the retry preserve? *Answer: the same operation identity and business effect, using provider-compatible deduplication and reconciliation as necessary.*

**D.** New code works but old clients still read the previous field. Is migration complete? *Answer: no. Verify compatibility and consumer migration before removing the old representation.*

## Revision checklist

- [ ] Explain read-time assembly versus materialization and their failure cases.
- [ ] Calculate polling and fan-out work with stated assumptions.
- [ ] Trace network, waiting, and processing intervals.
- [ ] Interpret p50 and p99 without confusing them with maxima.
- [ ] Explain valid aggregation across instances.
- [ ] Define a fault model and shared failure domains.
- [ ] Explain retry after commit but before response.
- [ ] Compare scaling approaches at a measured bottleneck.
- [ ] Explain the three maintainability principles through a safe change.

# Source notes

Primary: supplied *Designing Data-Intensive Applications*, second edition (2026), Chapter 2, printed pp. 33?56. Chapter body text and printed-page headings were inspected from a local extraction. The extractor reported malformed streams elsewhere in the PDF; this is not a claim that every book page extracted successfully.

Secondary: supplied Stack Learner Lecture 2, *Application Performance*, physical slides 6, 14?21, 27?34; Lecture 5, *System Reliability*, physical slides 7?14, 22?24, 30, 34?44. Course wording is reconciled explicitly where terminology differs. Other decks and security images are not asserted as sources for this handbook.

Original diagrams, implementation scenarios, calculations, proposed targets, and exercises are supplementary explanatory material. They illustrate concepts rather than reproduce production infrastructure or provide universal operational settings.
