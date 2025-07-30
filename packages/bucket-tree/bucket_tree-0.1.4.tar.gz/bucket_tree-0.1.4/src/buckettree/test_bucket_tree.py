import sys
import numpy as np
from buckettree.bucket_tree import BucketTree, Bucket


def test_bucket_initialization():
    bucket = Bucket(lo=-1.0, hi=1.0, is_leaf=False, level=2)
    assert isinstance(bucket.lo, float)
    assert bucket.lo == -1.0
    assert isinstance(bucket.hi, float)
    assert bucket.hi == 1.0
    assert isinstance(bucket.level, int)
    assert bucket.level == 2
    assert bucket.is_leaf == False  # noqa: E712


def test_bucket_bounds():
    caught = False
    try:
        bucket = Bucket(lo=10.0, hi=-10.0)
    except ValueError:
        caught = True
    assert caught

    caught = False
    try:
        bucket = Bucket(level=-3)  # noqa: F841
    except ValueError:
        caught = True
    assert caught


def test_bucket_tree_initialization():
    bt = BucketTree()
    assert bt.max_buckets == 100
    assert bt.n_buckets == 1
    assert bt.full == False  # noqa: E712
    assert bt.buckets[0] == bt.root
    assert bt.root.lo == -sys.float_info.max
    assert bt.root.hi == sys.float_info.max
    assert bt.root.is_leaf == True  # noqa: E712
    assert bt.root.level == 0

    assert bt.highs[0] == sys.float_info.max
    assert bt.lows[0] == -sys.float_info.max
    assert bt.leaves[0] == True  # noqa: E712
    assert bt.levels[0] == 0


def test_bucket_tree_bounds():
    caught = False
    try:
        bt = BucketTree(max_buckets=-100)  # noqa: F841
    except ValueError:
        caught = True
    assert caught


def test_bucket_tree_binning():
    bt = BucketTree(max_buckets=79)
    bin_membership = bt.bin(1.0)

    assert bt.n_buckets == 1
    assert bin_membership[0] == 1.0

    for _ in range(300_000):
        bin_memberships = bt.bin(np.random.sample())

    assert bt.n_buckets == 79
    assert np.where(bin_memberships > 0)[0].size > 1


def test_bucket_tree_binary():
    bt = BucketTree()
    for _ in range(1_000):
        bt.bin(np.random.randint(2))

    # There should only be 3 buckets, root and its two children, 0 and 1.
    assert bt.n_buckets == 3
