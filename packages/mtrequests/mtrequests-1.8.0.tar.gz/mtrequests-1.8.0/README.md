# mtrequests
threading for requests


```python
import mtrequests

pp = mtrequests.PendingPool()

print(mtrequests.get("https://example.com").send())
print(mtrequests.get("https://example.com").wrap(pp).send())
print(pp.wrap(mtrequests.get("https://example.com")).send())
```