import unittest
import sys
import os
from .context import *
from suristatsparser.common import *
from suristatsparser.ruleGroupParser import *
from suristatsparser.ruleGroupPerfParser import *
from suristatsparser.timestampedParser import *
import os
cwd = os.path.dirname(os.path.realpath(__file__))
text = "Date: 7/10/2024 -- 08:26:14 (uptime: 0d, 00h 00m 14s)"
class TestExtractWorks(unittest.TestCase):
    def test_extract_not_none(self):
        #expected 1720599974, 14
        result = parse_tstamp(text)
        self.assertIsNotNone(result)
    def test_extract_exact(self):
        #expected 1720599974, 14
        result = parse_tstamp(text)
        self.assertTupleEqual(result, (1720599974, 14))
    def test_extract_none(self):
        #expected 1720599974, 14
        result = parse_tstamp("UwU")
        self.assertIsNone(result)

class TestSkipDashline(unittest.TestCase):
    def test_skip_dashline(self):
        #expected True
        result = skip_dashline("----")
        self.assertTrue(result)
        self.assertTrue(skip_dashline("------------------------------------------------------------------------------------"))
    def test_not_skip_dashline(self):
        self.assertFalse(skip_dashline(" ----"))
        self.assertFalse(skip_dashline("--- "))
        self.assertFalse(skip_dashline("a --"))
        self.assertFalse(skip_dashline("adghkb---ada"))
    def test_skip_dashline_spaces(self):
        self.assertTrue(skip_dashline("    ----", allow_spaces=True))
        self.assertTrue(skip_dashline("  ---------  ------------ -----------  ------------- ---------- -------------- ---------------", allow_spaces=True))

class TestParseColumnHeaders(unittest.TestCase):
    def test_parse_column_headers(self):
        result = parse_column_headers("a | b | c")
        self.assertListEqual(result, ["a", "b", "c"])
    def test_parse_column_headers_no_space(self):
        result = parse_column_headers("a|b|c")
        self.assertListEqual(result, ["a", "b", "c"])
    def test_parse_column_headers_space(self):
        result = parse_column_headers(" a | b | c ")
        self.assertListEqual(result, ["a", "b", "c"])
    def test_parse_column_headers_empty(self):
        result = parse_column_headers("")
        self.assertListEqual(result, [])
    def test_parse_column_headers_words(self):
        result = parse_column_headers(" a | hello there | c ")
        self.assertListEqual(result, ["a", "hello there", "c"])
    def test_parse_column_sep_spaces(self):
        result = parse_column_headers(" hi there     b a   c ", sep="  ")
        self.assertListEqual(result, ["hi there", "b a", "c"])
class TestParseCounters(unittest.TestCase):
    in1 = r"decoder.pkts                                  | Total                     | 513537"
    def test_parse_counters(self):
        result = parse_counters(self.in1)
        self.assertTupleEqual(result, ("decoder.pkts", 513537))
simple_file = \
"""------------------------------------------------------------------------------------
Date: 7/10/2024 -- 08:26:13 (uptime: 0d, 00h 00m 13s)
------------------------------------------------------------------------------------
Counter                                       | TM Name                   | Value
------------------------------------------------------------------------------------
tcp.memuse                                    | Total                     | 9702184
tcp.reassembly_memuse                         | Total                     | 53240820
http.memuse                                   | Total                     | 763572
flow.memuse                                   | Total                     | 62395648
"""
class TestSimpleFile(unittest.TestCase):
    def test_simple_file(self):
        with open(f"{cwd}/testfile.txt", "w") as f:
            f.write(simple_file)
        with open(f"{cwd}/testfile.txt", "r") as f:
            parser = TimestampedCountersParser(f)
            result = parser.parse()
            self.assertListEqual(result, [
                ((1720599973, 13), ("tcp.memuse", 9702184)),
                ((1720599973, 13), ("tcp.reassembly_memuse", 53240820)),
                ((1720599973, 13), ("http.memuse", 763572)),
                ((1720599973, 13), ("flow.memuse", 62395648))
            ])
        os.remove(f"{cwd}/testfile.txt")
in1_parsed = [
    ((1720599973, 13), ("tcp.memuse", 9702184)),
    ((1720599973, 13), ("tcp.reassembly_memuse", 53240820)),
    ((1720599973, 13), ("http.memuse", 763572)),
    ((1720599973, 13), ("flow.memuse", 62395648))
]
class TestCollectCounters(unittest.TestCase):
    def test_simple(self):
        result = collect_counters(in1_parsed)
        self.assertListEqual(result, ['flow.memuse', 'http.memuse', 'tcp.memuse', 'tcp.reassembly_memuse'])

class TestRuleGroupParser(unittest.TestCase):
    def test_simple(self):
        file = f"{cwd}/rule_group_mini.json"
        rg = RuleGroupDB(file)
        self.assertEqual(len(rg.rule_groups), 8)
class TestRuleGroupPerfParser(unittest.TestCase):
    def test_simple(self):
        file = f"{cwd}/rule_group_perf.json"
        rg = RuleGroupPerfParser(file, use_json=True)
        self.assertTrue(5 in rg.rule_groups.keys())
        self.assertIsNotNone(rg.rule_groups[5].size_dist)


if __name__ == '__main__':
    unittest.main()