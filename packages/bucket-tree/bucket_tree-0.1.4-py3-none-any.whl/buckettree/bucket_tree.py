import sys
import numpy as np

MAX_VAL = sys.float_info.max
MIN_VAL = -sys.float_info.max


class BucketTree:
    def __init__(self, bucket_size=100, max_buckets=100):
        self.max_buckets = int(max_buckets)
        if self.max_buckets < 0:
            raise ValueError(
                f"'BucketTree.max_buckets' ({self.max_buckets}) "
                + "needs to be non-negative."
            )
        self.buckets = [None] * self.max_buckets
        self.full = False

        self.highs = np.zeros(self.max_buckets)
        self.lows = np.zeros(self.max_buckets)
        self.leaves = np.zeros(self.max_buckets, dtype=bool)
        self.levels = -np.ones(self.max_buckets, dtype=int)

        self.root = Bucket(bucket_size=bucket_size)
        i_root = 0
        self.root.i_bucket = i_root
        self.buckets[i_root] = self.root
        self.highs[i_root] = self.root.hi
        self.lows[i_root] = self.root.lo
        self.leaves[i_root] = True
        self.levels[i_root] = 0

        self.n_buckets = 1

    def bin(self, observation):
        """
        In it's current implementation, the set of observations for a bucket doesn't
        continue to update after the tree is full.
        This means that the distribution of observations will not reflect any
        evolution in the distribution over time. This is a trade off to help
        make the code run faster.

        To change this, modify the code so that
        it walks the tree during every iteration, regardless of self.full status.
        """
        # Ensure that the observation is a float.
        observation = float(observation)

        # If the tree isn't full yet, help it grow.
        # Find the leaf this observation belongs in and update it.
        if not self.full:
            leaf_bucket = self.root.observe(observation)
            success = leaf_bucket.attempt_split()
            # If successful, index the new buckets and put their info into
            # quick-to-access data structures.
            if success:
                lo_child = leaf_bucket.lo_child
                hi_child = leaf_bucket.hi_child
                i_lo = self.n_buckets
                i_hi = self.n_buckets + 1
                lo_child.i_bucket = i_lo
                hi_child.i_bucket = i_hi
                self.buckets[i_lo] = lo_child
                self.buckets[i_hi] = hi_child
                self.highs[i_lo] = lo_child.hi
                self.highs[i_hi] = hi_child.hi
                self.lows[i_lo] = lo_child.lo
                self.lows[i_hi] = hi_child.lo
                self.leaves[i_lo] = True
                self.leaves[i_hi] = True
                self.levels[i_lo] = lo_child.level
                self.levels[i_hi] = hi_child.level

                self.leaves[leaf_bucket.i_bucket] = False
                self.n_buckets += 2

                # Allow for the fact that two new buckets are created on each split.
                if self.n_buckets >= self.max_buckets - 1:
                    self.full = True

        # Find all the buckets this observation belongs in.
        bins = np.zeros(self.max_buckets)
        i_match = np.where(
            np.logical_and(
                observation >= self.lows[: self.n_buckets],
                observation < self.highs[: self.n_buckets],
            )
        )[0]

        # There should always be at least one matching bin.
        assert i_match.size > 0

        # Greedy membership is a debugging modification.
        _greedy_membership = False
        if _greedy_membership:
            # Assign all the membership to the leaf.
            # This is a simpler assignment method, but can be useful when
            # debugging and verifying that things should work as intended.
            memberships = np.zeros(i_match.size)
            i_leaf = np.argmax(self.levels[i_match])
            memberships[i_leaf] = 1.0
            bins[i_match] = memberships
        else:
            # Find the distribution of bucket memberships.
            # It sums to 1, distributed most heavily to the leaves.
            # Each level has twice the weight as the level before.
            bins[i_match] = 2 ** self.levels[i_match] / np.sum(
                2 ** self.levels[i_match]
            )

        return bins


class Bucket:
    def __init__(
        self,
        bucket_size=100,
        lo=MIN_VAL,
        hi=MAX_VAL,
        is_leaf=True,
        level=0,
        min_observation_range=1e-10,
        n_split_candidates=10,
    ):
        # The low and high limits of the range for this bucket.
        # The range is inclusive of the low value and exclusive of the high value.
        self.lo = float(lo)
        self.hi = float(hi)

        if self.hi <= self.lo:
            raise ValueError(
                f"'Bucket.hi' ({self.hi}) needs to be higher than 'Bucket.lo' ({self.lo})."
            )

        # The depth of the bucket tree at which this node sits.
        self.level = int(level)
        if self.level < 0:
            raise ValueError(f"'Bucket.level' ({self.level}) needs to be non-negative.")

        self.bucket_size = bucket_size
        self.n_observations = 0
        self.observations = np.zeros(self.bucket_size)
        self.is_leaf = is_leaf
        self.split_value = None
        self.lo_child = None
        self.hi_child = None

        self.n_split_candidates = n_split_candidates
        # self.split_countdown = self.bucket_size
        self.split_countdown = self.bucket_size * 2**self.level
        self.min_observation_range = min_observation_range

    def observe(self, observation):
        """
        Walk the tree to find the leaf bucket that contains the observation.

        Along the way, add the new value to observations in each bucket.
        Once complement of observations is full, randomly replace elements.
        This will ensure that the distribution of observations will be
        approximately correct, even if it evolves over time.
        """
        if self.n_observations >= self.bucket_size:
            i_observation = np.random.randint(self.bucket_size)
        else:
            i_observation = self.n_observations
        self.observations[i_observation] = observation

        self.n_observations += 1
        self.split_countdown -= 1

        if self.is_leaf:
            leaf_bucket = self
        else:
            if observation < self.split_value:
                leaf_bucket = self.lo_child.observe(observation)
            else:
                leaf_bucket = self.hi_child.observe(observation)

        return leaf_bucket

    def attempt_split(self):
        """
        Figure out whether it's time to split this bucket.

        Returns True if successful, False otherwise
        """
        if self.split_countdown > 0:
            return False

        split_value = None
        self.split_countdown = self.bucket_size * 2**self.level

        # Check that max - min is larger than some infinitessimal value.
        max_observation = np.max(self.observations)
        min_observation = np.min(self.observations)
        if max_observation - min_observation < self.min_observation_range:
            # If there is no spread in the observations, go back and collect
            # some more observations and try again later.
            # For sparse or time varying sensors
            # this can take a long time to show up.
            return False

        # else:
        #     There is a viable split in this group of observations.

        # Generate split candidates that are evenly spaced along the range
        # of observations, but do not include either extreme.
        candidates = np.linspace(
            min_observation, max_observation, self.n_split_candidates + 2
        )[1:-1]

        # Calculate the split error for each candidate.
        # Lower error indicates a higher quality split, and zero is perfect.
        # In cases where there are multiple splits that are equally good,
        # Pick the split that is the closest to the midpoint of the means
        # of the low and high groups.
        errors = np.zeros(candidates.size)
        tiebreakers = np.zeros(candidates.size)
        # This is not very efficient Python code, but it's short and it doesn't
        # get run very often. It is optimized for readability.
        for i_cand, cand in enumerate(candidates):
            # Split the observations into values that fall below the
            # candidate and those that fall above.
            i_lo = np.where(self.observations < cand)[0]
            i_hi = np.where(self.observations >= cand)[0]
            # Find the total R^2,
            # the sum of (x - mean)^2 for both sides of the split.
            lo_mean = np.mean(self.observations[i_lo])
            hi_mean = np.mean(self.observations[i_hi])
            lo_R2 = np.sum((self.observations[i_lo] - lo_mean) ** 2)
            hi_R2 = np.sum((self.observations[i_hi] - hi_mean) ** 2)
            errors[i_cand] = lo_R2 + hi_R2
            tiebreakers[i_cand] = (lo_mean - cand) ** 2 + (hi_mean - cand) ** 2

        min_error = np.min(errors)
        i_best_splits = np.where(errors == min_error)[0]
        i_tiebreaker = np.argmin(tiebreakers[i_best_splits])
        split_value = candidates[i_best_splits[i_tiebreaker]]

        # Take care of the split.
        self.is_leaf = False
        self.split_value = split_value

        # Create the children.
        self.lo_child = Bucket(
            bucket_size=self.bucket_size,
            lo=self.lo,
            hi=self.split_value,
            level=self.level + 1,
        )
        i_lo_obs = np.where(self.observations < self.split_value)[0]
        n_lo_obs = i_lo_obs.size
        self.lo_child.observations[:n_lo_obs] = self.observations[i_lo_obs]
        self.lo_child.n_observations = n_lo_obs

        self.hi_child = Bucket(
            bucket_size=self.bucket_size,
            lo=self.split_value,
            hi=self.hi,
            level=self.level + 1,
        )
        i_hi_obs = np.where(self.observations >= self.split_value)[0]
        n_hi_obs = i_hi_obs.size
        self.hi_child.observations[:n_hi_obs] = self.observations[i_hi_obs]
        self.hi_child.n_observations = n_hi_obs

        return True


if __name__ == "__main__":
    import time
    import buckettree.viewer as btv

    # Smoke test
    bt = BucketTree()

    start = time.time()
    n_iter = 10_000
    for _ in range(n_iter):
        bt.bin(np.random.sample())
    elapsed = time.time() - start
    print(f"{int(1e6 * elapsed / n_iter)} us per observation")

    print(f"BucketTree has {bt.n_buckets} buckets")
    i_bucket = np.random.randint(bt.n_buckets)
    print(f"Randomly selected bucket {i_bucket} has")
    print(f"    lo = {bt.lows[i_bucket]}")
    print(f"    hi = {bt.highs[i_bucket]}")
    print(f"    level = {bt.levels[i_bucket]}")
    print(f"    is_leaf = {bt.leaves[i_bucket]}")

    btv.view(bt)
