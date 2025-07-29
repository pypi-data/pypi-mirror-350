"""Main module."""

import logging
import itertools
import re
import numpy as np
from typing import Union
from collections import OrderedDict

try:
    import pandas as pd

    logging.debug("pandas imported")
except Exception:
    pass
try:
    import polars as pl

    logging.debug("polars imported")
except Exception:
    import pandas as pl

from .grammar import (
    rule_expression,
)
from .parser import RuleParser
from .evaluator import CodeEvaluator
from .pandas_parser import (
    dataframe_index,
    dataframe_values,
)
from .utils import (
    flatten,
    generate_substitutions,
    is_column,
    is_string,
)
from .metrics import (
    metrics,
    required_variables,
    calculate_metrics,
    add_required_variables,
)
from .const import (
    CONFIDENCE,
    ABSOLUTE_SUPPORT,
    ABSOLUTE_EXCEPTIONS,
    NOT_APPLICABLE,
    RULE_ID,
    RULE_GROUP,
    RULE_DEF,
    RESULT,
    INDICES,
    ENCODINGS,
    VAR_X_AND_Y,
    VAR_NOT_X,
    VAR_X_AND_NOT_Y,
    LOG,
)


class RuleMiner:
    """
    The RuleMiner object contains rules and data

    It used three basic functions:
    - update (rule expressions, rules or data)
    - generate (rules from templates (with regexes) and data)
    - convert (do not generate but only convert rules (without regexes))
    - evaluate (results from rule)

    It uses a RuleParser and a CodeEvaluator

    """

    def __init__(
        self,
        templates: list = None,
        rules: Union[pd.DataFrame, pl.DataFrame] = None,
        data: Union[pd.DataFrame, pl.DataFrame] = None,
        params: dict = None,
    ):
        """ """
        self.params = dict()
        self.parser = RuleParser()
        self.evaluator = CodeEvaluator(params)
        self.update(templates=templates, rules=rules, data=data, params=params)

    def update(
        self,
        templates: list = None,
        rules: Union[pd.DataFrame, pl.DataFrame] = None,
        data: Union[pd.DataFrame, pl.DataFrame] = None,
        params: dict = None,
    ) -> None:
        """
        Updates the internal state of the object with new parameters, data, templates, and rules.

        This method allows the user to modify various aspects of the object, such as updating the
        data used for analysis, setting new parameters, and specifying templates and rules for
        further processing. It performs validation of certain parameters and ensures the correct
        setup for evaluating rules based on the provided data.

        Args:
            templates (list, optional): A list of templates to use for the analysis. If provided,
                                         the method will generate new results using these templates.
            rules (Union[pd.DataFrame, pl.DataFrame], optional): A DataFrame containing the rules
                                                                  to evaluate. If provided, the method
                                                                  will evaluate the rules based on the
                                                                  current data.
            data (Union[pd.DataFrame, pl.DataFrame], optional): A DataFrame containing the data to
                                                                 be used in the analysis. If provided,
                                                                 the method will update the internal
                                                                 data and reinitialize the parser and
                                                                 evaluator.
            params (dict, optional): A dictionary of parameters to configure the analysis. This can
                                      include metrics, filters, tolerance settings, and the
                                      desired data types for rules and results. If provided,
                                      the method will apply these parameters to update the state.

        Raises:
            Exception: If the "tolerance" parameter is provided and it does not contain a 'default'
                      key, or if any key in the tolerance dictionary contains spaces.

        Returns:
            None: This method does not return any value but updates the internal state of the object
                  based on the input parameters.
        """
        if params is not None:
            self.params = params
            self.parser.set_params(params)
            self.evaluator.set_params(params)

        self.data = data
        self.parser.set_data(data)
        self.evaluator.set_data(data)

        self.metrics = self.params.get(
            "metrics",
            [ABSOLUTE_SUPPORT, ABSOLUTE_EXCEPTIONS, CONFIDENCE, NOT_APPLICABLE],
        )
        self.metrics = metrics(self.metrics)
        self.required_vars = required_variables(self.metrics)
        self.filter = self.params.get("filter", {CONFIDENCE: 0.5, ABSOLUTE_SUPPORT: 2})
        self.tolerance = self.params.get("tolerance", None)
        if self.tolerance is not None:
            if "default" not in self.tolerance.keys():
                raise Exception("No 'default' key found in tolerance definition.")
            for key in self.tolerance.keys():
                if " " in key:
                    raise Exception(
                        "No spaces allowed in keys of tolerance definition."
                    )
        self.rules_datatype = self.params.get("rules_datatype", pd.DataFrame)
        self.results_datatype = self.params.get("results_datatype", pd.DataFrame)

        if templates is not None:
            self.templates = templates
            self.generate()

        if rules is not None:
            self.rules = rules
            self.evaluate()

        return None

    def generate(self) -> None:
        """
        Generates rules based on the defined templates and available data.

        This method checks if templates are defined and, depending on whether data is available,
        either converts the templates into rules or generates rules using the provided templates
        and data. If no templates are defined, an assertion error is raised.

        Raises:
            AssertionError: If no templates are defined when attempting to generate rules.

        Returns:
            None: This method does not return any value but updates the internal state by generating
                  the rules based on the templates and data.
        """
        assert (
            self.templates is not None
        ), "Unable to generate rules, no templates defined."

        self.rules = None
        if self.data is None:
            self.convert(templates=self.templates)
        else:
            self.generate_rules(templates=self.templates)

        return None

    def evaluate(
        self,
        data: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Evaluates the defined rules on the given data and returns the results.

        This method performs rule evaluation based on the provided data and previously defined
        rules. If no data is provided, it will use the current data. For each rule, the method
        computes metrics (such as absolute support, exceptions, and confidence) and determines
        whether the rule is satisfied (confirmation), violated (exception), or not applicable.
        The results are organized in a DataFrame or a specified data format.

        Args:
            data (pd.DataFrame, optional): A DataFrame containing the data to evaluate. If not
                                            provided, the method uses the current data stored in
                                            the object.

        Returns:
            pd.DataFrame: A DataFrame containing the evaluation results with columns for rule id,
                          rule group, rule definition, status, metrics (support, exceptions,
                          confidence), result (True/False/None), and indices.

        Raises:
            AssertionError: If no rules are defined or no data is available for evaluation.
        """
        logger = logging.getLogger(__name__)
        if data is not None:
            self.update(data=data)

        assert self.rules is not None, "Unable to evaluate data, no rules defined."
        assert self.data is not None, "Unable to evaluate data, no data defined."

        results = OrderedDict(
            {
                RULE_ID: [],
                RULE_GROUP: [],
                RULE_DEF: [],
                ABSOLUTE_SUPPORT: [],
                ABSOLUTE_EXCEPTIONS: [],
                CONFIDENCE: [],
                NOT_APPLICABLE: [],
                RESULT: [],
                INDICES: [],
                LOG: [],
            }
        )

        mapping_dtypes = {
            RULE_ID: self.rules[RULE_ID].dtype,
            RULE_GROUP: self.rules[RULE_GROUP].dtype,
            RULE_DEF: self.rules[RULE_DEF].dtype,
            ABSOLUTE_SUPPORT: "Int64",
            ABSOLUTE_EXCEPTIONS: "Int64",
            CONFIDENCE: "Float64",
            NOT_APPLICABLE: "Int64",
            RESULT: "object",
            INDICES: "object",
            LOG: "object",
        }

        if self.params.get("apply_rules_on_indices", True):
            # add temporary index columns (to allow rules based on index data)
            for level in range(len(self.data.index.names)):
                self.data[str(self.data.index.names[level])] = (
                    self.data.index.get_level_values(level=level)
                )

        for rule_idx, row in self.rules.iterrows():
            rule_id = row[RULE_ID]
            rule_def = row[RULE_DEF]
            rule_group = row[RULE_GROUP]
            rule_code = dataframe_index(expression=rule_def, data=self.data)
            code_results, code_log = self.evaluator.evaluate_dict(
                expressions=rule_code, encodings={}
            )
            code_results = add_required_variables(
                required_vars=self.required_vars,
                results=code_results,
            )
            len_results = {
                key: len(code_results[key])
                if not isinstance(code_results[key], float)
                else 0
                for key in code_results.keys()
                if code_results[key] is not None
            }
            rule_metrics = calculate_metrics(
                len_results=len_results,
                metrics=self.metrics,
            )

            co_indices = code_results[VAR_X_AND_Y]
            ex_indices = code_results[VAR_X_AND_NOT_Y]
            na_indices = code_results[VAR_NOT_X]
            if code_log is not None:
                co_log = code_log.get(code_results[VAR_X_AND_Y], "")
                ex_log = code_log.get(code_results[VAR_X_AND_NOT_Y], "")
                # na_log = code_log[VAR_NOT_X]

            if co_indices is not None and not isinstance(co_indices, float):
                nco = len(co_indices)
            else:
                nco = 0
            if ex_indices is not None and not isinstance(ex_indices, float):
                nex = len(ex_indices)
            else:
                nex = 0
            if na_indices is not None and not isinstance(na_indices, float):
                nna = len(na_indices)
            else:
                nna = 0

            if self.params.get("output_confirmations", True):
                if nco > 0:
                    results[RULE_ID].extend([rule_id] * nco)
                    results[RULE_GROUP].extend([rule_group] * nco)
                    results[RULE_DEF].extend([rule_def] * nco)
                    results[ABSOLUTE_SUPPORT].extend(
                        [rule_metrics[ABSOLUTE_SUPPORT]] * nco
                    )
                    results[ABSOLUTE_EXCEPTIONS].extend(
                        [rule_metrics[ABSOLUTE_EXCEPTIONS]] * nco
                    )
                    results[CONFIDENCE].extend([rule_metrics[CONFIDENCE]] * nco)
                    results[NOT_APPLICABLE].extend([rule_metrics[NOT_APPLICABLE]] * nco)
                    results[RESULT].extend([True] * nco)
                    results[INDICES].extend(co_indices)
                    results[LOG].extend(
                        co_log if code_log is not None else [None] * nco
                    )

            if self.params.get("output_exceptions", True):
                if nex > 0:
                    results[RULE_ID].extend([rule_id] * nex)
                    results[RULE_GROUP].extend([rule_group] * nex)
                    results[RULE_DEF].extend([rule_def] * nex)
                    results[ABSOLUTE_SUPPORT].extend(
                        [rule_metrics[ABSOLUTE_SUPPORT]] * nex
                    )
                    results[ABSOLUTE_EXCEPTIONS].extend(
                        [rule_metrics[ABSOLUTE_EXCEPTIONS]] * nex
                    )
                    results[CONFIDENCE].extend([rule_metrics[CONFIDENCE]] * nex)
                    results[NOT_APPLICABLE].extend([rule_metrics[NOT_APPLICABLE]] * nex)
                    results[RESULT].extend([False] * nex)
                    results[INDICES].extend(ex_indices)
                    results[LOG].extend(
                        ex_log if code_log is not None else [None] * nex
                    )

            if self.params.get("output_not_applicable", False):
                if (nco == 0 and nex == 0) and nna > 0:
                    results[RULE_ID].extend([rule_id])
                    results[RULE_GROUP].extend([rule_group])
                    results[RULE_DEF].extend([rule_def])
                    results[ABSOLUTE_SUPPORT].extend([rule_metrics[ABSOLUTE_SUPPORT]])
                    results[ABSOLUTE_EXCEPTIONS].extend(
                        [rule_metrics[ABSOLUTE_EXCEPTIONS]]
                    )
                    results[CONFIDENCE].extend([rule_metrics[CONFIDENCE]])
                    results[NOT_APPLICABLE].extend([rule_metrics[NOT_APPLICABLE]])
                    results[RESULT].extend([None])
                    results[INDICES].extend([None])
                    results[LOG].extend([None])

            logger.info(
                "Finished: "
                + str(rule_idx)
                + " ("
                + str(rule_id)
                + ", "
                + str(rule_group)
                + ")"
                + " ["
                + str(nco)
                + " confirmations and "
                + str(nex)
                + " exceptions]"
            )

        if self.results_datatype == pd.DataFrame:
            self.results = pd.DataFrame.from_dict(results).astype(mapping_dtypes)
        elif self.results_datatype == pl.DataFrame:
            self.results = pl.DataFrame(results)
        elif isinstance(self.results_datatype, dict):
            self.results = results

        if self.params.get("apply_rules_on_indices", True):
            # remove temporarily added index columns
            for level in range(len(self.data.index.names)):
                del self.data[str(self.data.index.names[level])]

        return self.results

    def convert(self, templates: list = []) -> None:
        """
        Converts a list of templates into a set of rules

        This method processes a list of templates, extracting and converting each one into a rule
        expression in the form of an "if then" rule. The resulting rules are stored in the internal
        `rules` object, which can be either a Pandas DataFrame or a Polars DataFrame, depending on
        the configuration. The method also handles error cases related to parsing template expressions.

        Args:
            templates (list, optional): A list of templates to convert into rules. Each template
                                         should be a dictionary containing at least the key `expression`
                                         with a string representing the rule's condition. Other optional
                                         keys are `group` and `encodings` (rule-specific encodings).

        Returns:
            None: This method does not return any value. It updates the internal `rules` object with
                  the generated rules based on the provided templates.

        Raises:
            Exception: If there is a parsing error in the template expression, an error is logged,
                      and the method returns `None` without updating the rules.
        """
        logger = logging.getLogger(__name__)

        # if the template expression is not a if then rule then it is changed
        # into an if then rule

        # create dict of lists for rules
        rules = OrderedDict(
            {
                **{
                    RULE_ID: [],
                    RULE_GROUP: [],
                    RULE_DEF: [],
                },
                **{metric: [] for metric in self.metrics},
                **{ENCODINGS: []},
            }
        )

        # determine rule_id
        if self.rules is not None:
            if self.rules_datatype == pd.DataFrame:
                rule_id = len(self.rules.index)
            elif self.rules_datatype == pl.DataFrame:
                rule_id = self.rules.select(pl.len())[0, 0]
        else:
            rule_id = 0

        for template in templates:
            group = template.get("group", 0)
            encodings = template.get("encodings", {})
            template_expression = template.get("expression", None)
            try:
                condition = re.compile(r"if(.*)then(.*)", re.IGNORECASE)
                rule_parts = condition.search(template_expression)
                if rule_parts is None:
                    template_expression = "if () then " + template_expression
                parsed = (
                    rule_expression()
                    .parse_string(template_expression, parseAll=True)
                    .as_list()
                )
            except Exception as e:
                logger.error("Parsing error in " + repr(template_expression))
                logger.debug("Parsing error message: " + repr(e))
                return None
            reformulated_expression = self.parser.parse(parsed)

            rules[RULE_ID].append(rule_id)
            rules[RULE_GROUP].append(group)
            rules[RULE_DEF].append(reformulated_expression)
            for metric in self.metrics:
                rules[metric].append(np.nan)
            rules[ENCODINGS].append(encodings)

            rule_id += 1

        if self.rules_datatype == pd.DataFrame:
            self.rules = pd.DataFrame.from_dict(rules)
        elif self.rules_datatype == pl.DataFrame:
            self.rules = pl.DataFrame(rules)

    def generate_rules(self, templates: list) -> None:
        """
        Generate all rules given a list of templates

        """
        for template in templates:
            self.generate_rule(template)

    def generate_rule(self, template: dict) -> None:
        """
        Generates a rule from a template and adds it to the internal rules set.

        This method processes a single template to create a rule expression in the "if then"
        format. It handles parsing the template expression, applying substitutions to the "if"
        and "then" parts, and evaluating the rule against the current data. The resulting rule
        is added to the internal set of rules, and the rule's metrics are calculated. The method
        also handles the temporary addition of index names as columns for rule derivation.

        Args:
            template (dict): A dictionary representing the template to be converted into a rule.
                              It should include the following keys:
                              - "expression" (str): The rule expression in string form (e.g., "if ... then ...").
                              - "group" (int, optional): The group ID for the rule.
                              - "encodings" (dict, optional): Additional encodings related to the rule.

        Returns:
            None: This method does not return a value. It updates the internal `rules` object with
                  the generated rule.

        Raises:
            Exception: If there is a parsing error in the template expression, an error is logged,
                      and the method will not generate or add the rule to the internal rules set.
        """
        logger = logging.getLogger(__name__)

        group = template.get("group", 0)
        encodings = template.get("encodings", {})
        template_expression = template.get("expression", None)

        if self.params.get("apply_rules_on_indices", True):
            # temporarily add index names as columns, so we derive rules with index names
            if self.data is not None:
                for level in range(len(self.data.index.names)):
                    self.data[str(self.data.index.names[level])] = (
                        self.data.index.get_level_values(level=level)
                    )

        # create dict of lists for rules
        rules = OrderedDict(
            {
                **{
                    RULE_ID: [],
                    RULE_GROUP: [],
                    RULE_DEF: [],
                },
                **{metric: [] for metric in self.metrics},
                **{ENCODINGS: []},
            }
        )

        # determine rule_id
        if self.rules is not None:
            if self.rules_datatype == pd.DataFrame:
                rule_id = len(self.rules.index)
            elif self.rules_datatype == pl.DataFrame:
                rule_id = self.rules.select(pl.len())[0, 0]
        else:
            rule_id = 0

        # if the template expression is not a if then rule then it is changed
        # into an if then rule
        try:
            parsed, if_part, then_part = self.split_rule(expression=template_expression)
        except Exception as e:
            logger.error("Parsing error in expression " + repr(template_expression))
            logger.debug("Parsing error message: " + repr(e))
            return None

        sorted_expressions = {}

        if_part_column_values = self.search_column_value(if_part, [])
        if_part_substitutions = [
            generate_substitutions(df=self.data, column_value=column_value)
            for column_value in if_part_column_values
        ]
        if_part_substitutions = itertools.product(*if_part_substitutions)

        logger.info("Expression for if-part (" + str(if_part) + ") generated")
        for if_part_substitution in if_part_substitutions:
            candidate, _, _, _, _ = self.substitute_list(
                expression=if_part,
                columns=[item[0] for item in if_part_column_values],
                values=[item[1] for item in if_part_column_values],
                column_substitutions=[item[0] for item in if_part_substitution],
                value_substitutions=[item[1] for item in if_part_substitution],
            )
            candidate = self.parser.parse(candidate)
            df_code = dataframe_values(expression=flatten(candidate), data=self.data)
            df_eval, _ = self.evaluator.evaluate_str(expression=df_code, encodings={})
            if not isinstance(df_eval, float):  # then it is nan
                # substitute variables in then_part
                then_part_substituted = self.substitute_group_names(
                    then_part, [item[2] for item in if_part_substitution]
                )
                then_part_column_values = self.search_column_value(
                    then_part_substituted, []
                )
                then_part_substitutions = [
                    generate_substitutions(df=df_eval, column_value=column_value)
                    for column_value in then_part_column_values
                ]
                if if_part_substitution != ():
                    expression_substitutions = [
                        if_part_substitution + item
                        for item in itertools.product(*then_part_substitutions)
                    ]
                else:
                    expression_substitutions = list(
                        itertools.product(*then_part_substitutions)
                    )
                template_column_values = if_part_column_values + then_part_column_values

                candidates = []
                if expression_substitutions == []:
                    # no substitutions, so original parsed expression
                    candidates.append(parsed)
                else:
                    # add all substitutions to candidate list
                    for substitution in expression_substitutions:
                        # substitute variables in full expression
                        parsed_substituted = self.substitute_group_names(
                            parsed, [item[2] for item in substitution]
                        )
                        candidate_parsed, _, _, _, _ = self.substitute_list(
                            expression=parsed_substituted,
                            columns=[item[0] for item in template_column_values],
                            values=[item[1] for item in template_column_values],
                            column_substitutions=[item[0] for item in substitution],
                            value_substitutions=[item[1] for item in substitution],
                        )
                        candidates.append(candidate_parsed)

                for candidate in candidates:
                    sorted_expression = flatten_and_sort(candidate)
                    reformulated_expression = self.parser.parse(candidate)
                    if sorted_expression not in sorted_expressions.keys():
                        sorted_expressions[sorted_expression] = True
                        rule_code = dataframe_index(
                            expression=reformulated_expression,
                            data=self.data,
                        )
                        code_results, _ = self.evaluator.evaluate_dict(
                            expressions=rule_code, encodings={}
                        )
                        code_results = add_required_variables(
                            required_vars=self.required_vars,
                            results=code_results,
                        )
                        len_results = {
                            key: len(code_results[key])
                            if not isinstance(code_results[key], float)
                            else 0
                            for key in code_results.keys()
                            if code_results[key] is not None
                        }
                        rule_metrics = calculate_metrics(
                            len_results=len_results, metrics=self.metrics
                        )

                        logger.debug(
                            "Rule code: \n"
                            + str(
                                "\n".join(
                                    [key + ": " + s for key, s in rule_code.items()]
                                )
                            )
                        )
                        logger.debug(
                            "Candidate expression "
                            + reformulated_expression
                            + " has rule metrics "
                            + str(rule_metrics)
                        )
                        if self.apply_filter(metrics=rule_metrics):
                            rules[RULE_ID].append(rule_id)
                            rules[RULE_GROUP].append(group)
                            rules[RULE_DEF].append(reformulated_expression)
                            for metric, value in rule_metrics.items():
                                rules[metric].append(value)
                            rules[ENCODINGS].append(encodings)

                            rule_id += 1

        if self.rules_datatype == pd.DataFrame:
            self.rules = pd.DataFrame.from_dict(rules)
        elif self.rules_datatype == pl.DataFrame:
            self.rules = pl.DataFrame(rules)

        if self.params.get("apply_rules_on_indices", True):
            # remove temporarily added index columns
            if self.data is not None:
                for level in range(len(self.data.index.names)):
                    del self.data[str(self.data.index.names[level])]

    def substitute_group_names(
        self, expr: str = None, group_names_list: list = []
    ) -> list:
        """
        Substitute group names in an expression.

        This method substitutes placeholders in an expression with their
        corresponding group names. Group names are provided as a list,
        and placeholders in the expression are represented as '\x01',
        '\x02', and so on. The method replaces these placeholders with
        the group names from the list.

        Args:
            expr (str or list): The expression or list of expressions to
            be processed.
            group_names_list (list): A list of group names to use as
            substitutions.

        Returns:
            str or list: The expression with placeholders replaced by group names.

        Example:
            expression = "Column '\x01' contains values from group '\x02'"

            group_names = ['Group A', 'Numbers']

            result = ruleminer.RuleMiner().substitute_group_names(expression, group_names)

            print(result)

                "Column 'Group A' contains values from group 'Numbers'"

        Note:
            The method can be applied to both strings and lists of expressions.
            It searches for placeholders in the format '\x01', '\x02', and so on,
            and substitutes them with the corresponding group names from the list.
        """
        if isinstance(expr, str):
            for group_names in group_names_list:
                if group_names is not None:
                    for idx, key in enumerate(group_names):
                        expr = re.sub("\\x0" + str(idx + 1), key, expr)
            return expr
        elif isinstance(expr, list):
            return [self.substitute_group_names(i, group_names_list) for i in expr]

    def search_column_value(self, expr, column_value) -> list:
        """
        Search for column-value pairs in an expression.

        This method recursively searches for column-value pairs within an
        expression and appends them to the provided list. It identifies
        column-value pairs by checking the structure of the expression.

        Args:
            expr (str or list): The expression to search for column-value
            pairs.
            column_value (list): A list to store the identified column-value
            pairs.

        Returns:
            list: A list containing the discovered column-value pairs as tuples.

        Example:
            expression = ['{"A"}', '==', '"b"']

            column_value_pairs = ruleminer.RuleMiner().search_column_value(expression, [])

            print(column_value_pairs)

                [('{"A"}', '"b"')]

        Note:
            The method examines the structure of the expression and identifies
            column-value pairs by checking for specific patterns. It recursively
            traverses the expression to find such pairs and appends them to the
            provided list.
        """
        if isinstance(expr, str):
            if is_column(expr):
                column_value.append((expr, None))
        elif isinstance(expr, list):
            if len(expr) == 5 and is_column(expr[1]) and is_string(expr[3]):
                column_value.append((expr[1], expr[3]))
            elif len(expr) == 5 and is_column(expr[3]) and is_string(expr[1]):
                column_value.append((expr[3], expr[1]))
            else:
                for item in expr:
                    self.search_column_value(item, column_value)
        return column_value

    def split_rule(self, expression: str = "") -> tuple:
        """
        Split a rule expression into its 'if' and 'then' parts.

        This method takes a rule expression and splits it into its 'if' and
        'then' components. It uses regular expressions to identify these parts,
        and if the 'if' part is empty, it is assumed to be the entire rule
        expression. The resulting 'if' and 'then' parts are parsed and returned
        as lists.

        Args:
            expression (str): The rule expression to be split.

        Returns:
            tuple: A tuple containing the following elements:
                - list: The parsed rule expression as a list.
                - list: The 'if' part of the rule as a parsed list (empty
                  if not present).
                - list: The 'then' part of the rule as a parsed list.

        Example:
            rule_expression = 'if ({"A"} > 10) then ({"B"} == "C")'

            parsed, if_part, then_part = split_rule(rule_expression)

            print(parsed)

                ['if', ['{"A"}', '>', '10'], 'then', ['{"B"}', '==', '"C"']]

            print(if_part)

                [['{"A"}', '>', '10']]

            print(then_part)

                [['{"B"}', '==', '"C"']]

        Note:
            The method employs regular expressions to identify 'if' and 'then'
            parts, and if the 'if' part is not present, the entire expression
            is considered the 'then' part. The parsed results are returned as
            lists for further evaluation.
        """
        condition = re.compile(r"if(.*)then(.*)", re.IGNORECASE)
        rule_parts = condition.search(expression)
        if rule_parts is not None:
            if rule_parts.group(1).strip() != "()":
                if_part = (
                    rule_expression()
                    .parse_string(rule_parts.group(1), parseAll=True)
                    .as_list()
                )
            else:
                if_part = ""
            then_part = (
                rule_expression()
                .parse_string(rule_parts.group(2), parseAll=True)
                .as_list()
            )
        else:
            expression = "if () then " + expression
            if_part = ""
            then_part = (
                rule_expression().parse_string(expression, parseAll=True).as_list()
            )
        parsed = rule_expression().parse_string(expression, parseAll=True).as_list()
        return parsed, if_part, then_part

    def substitute_list(
        self,
        expression: str = "",
        columns: list = [],
        values: list = [],
        column_substitutions: list = [],
        value_substitutions: list = [],
    ):
        """
        Substitute columns and values in an expression with their substitutions.

        This method allows for the substitution of columns and values within an
        expression using the provided lists of column and value substitutions.
        It recursively processes the expression, replacing the first occurrence
        of a column or value with its substitution.

        Args:
            expression (str or list): The input expression to be processed.
            columns (list): A list of original columns to be substituted.
            values (list): A list of original values to be substituted.
            column_substitutions (list): A list of column substitutions.
            value_substitutions (list): A list of value substitutions.

        Returns:
            tuple: A tuple containing the following elements:
                - str or list: The processed expression with substitutions.
                - list: The remaining columns for substitution.
                - list: The remaining values for substitution.
                - list: The remaining column substitutions.
                - list: The remaining value substitutions.

        Example:
            expression = '({"A.*"} > 10) & ({"B.*"} == 20)'

            columns = ['{"A.*"}', {"B.*"}]

            values = [10, 20]

            column_subs = ["Aa", "Bb"]

            value_subs = [30, 40]

            result = ruleminer.RuleMiner().substitute_list(expression, columns, values, column_subs, value_subs)

            print(result)

                ('({"Aa"} > 10) & ({"B.*"} == 20)', [{'B.*'}], [10, 20], ['Bb'], [30, 40])

        """

        if isinstance(expression, str):
            if columns != [] and columns[0] in expression:
                # replace only first occurrence in string
                return (
                    expression.replace(
                        columns[0], '{"' + column_substitutions[0] + '"}', 1
                    ),
                    columns[1:],
                    values,
                    column_substitutions[1:],
                    value_substitutions,
                )
            elif values != [] and values[0] is not None and values[0] in expression:
                return (
                    expression.replace(
                        values[0], '"' + value_substitutions[0] + '"', 1
                    ),
                    columns,
                    values[1:],
                    column_substitutions,
                    value_substitutions[1:],
                )
            elif values != [] and values[0] is None:
                return (
                    expression,
                    columns,
                    values[1:],
                    column_substitutions,
                    value_substitutions[1:],
                )
            else:
                return (
                    expression,
                    columns,
                    values,
                    column_substitutions,
                    value_substitutions,
                )
        else:
            r = []
            for item in expression:
                (
                    item_s,
                    columns,
                    values,
                    column_substitutions,
                    value_substitutions,
                ) = self.substitute_list(
                    expression=item,
                    columns=columns,
                    values=values,
                    column_substitutions=column_substitutions,
                    value_substitutions=value_substitutions,
                )
                r.append(item_s)
            return (
                r,
                columns,
                values,
                column_substitutions,
                value_substitutions,
            )

    def apply_filter(self, metrics: dict = {}):
        """
        This function applies the filter to the rule metrics (for example
        confidence > 0.75)
        """
        return self.data is None or all(
            [metrics[metric] >= self.filter[metric] for metric in self.filter]
        )


def flatten_and_sort(expression: str = ""):
    """
    Recursively flatten and sort a nested expression and return it as a string.

    This function takes an expression, which can be a nested list of strings
    or a single string, and recursively flattens and sorts it into a single
    string enclosed in parentheses. Sorting is applied to certain elements
    within the expression, such as mathematical operations, column references,
    and strings, based on their relationships and order of precedence.

    Args:
        expression (str or list): The expression to be flattened and sorted.

    Returns:
        str: The flattened and sorted expression as a string enclosed in
        parentheses.

    Example:
        expression = ["max", ["C", "A"]]

        result = ruleminer.flatten_and_sort(expression)

        print(result)

            "(max((CA)))"

        expression = ["C", "==", ["A", "+", "B"]]

        result = ruleminer.flatten_and_sort(expression)

        print(result)

            "((A+B)==C)"
    """
    if isinstance(expression, str):
        return expression
    else:
        if isinstance(expression[0], str) and expression[0].lower() in [
            "min",
            "max",
        ]:
            res = (
                expression[0]
                + "("
                + "".join(sorted([flatten_and_sort(item) for item in expression[1:]]))
                + ")"
            )
        elif all(
            [is_string(item) or is_column(item) or item == "," for item in expression]
        ):
            return "".join(sorted(expression))
        else:
            # find elements to sort, sort then and add sorted to string
            idx_to_sort = set()
            for idx, item in enumerate(expression):
                if isinstance(item, str) and (item in ["==", "!="]):
                    idx_to_sort.add(idx - 1)
                    idx_to_sort.add(idx + 1)
                elif isinstance(item, str) and (item == "*"):
                    idx_to_sort.add(idx - 1)
                    idx_to_sort.add(idx + 1)
                elif (
                    isinstance(item, str) and (item == "+") and ("*" not in expression)
                ):
                    idx_to_sort.add(idx - 1)
                    idx_to_sort.add(idx + 1)
                elif isinstance(item, str) and (item == "&"):
                    idx_to_sort.add(idx - 1)
                    idx_to_sort.add(idx + 1)
                elif (
                    isinstance(item, str) and (item == "|") and ("&" not in expression)
                ):
                    idx_to_sort.add(idx - 1)
                    idx_to_sort.add(idx + 1)
            sorted_items = sorted(
                [flatten_and_sort(expression[i]) for i in list(idx_to_sort)]
            )

            res = ""
            count = 0
            for idx, item in enumerate(expression):
                if idx in idx_to_sort:
                    res += sorted_items[count]
                    count += 1
                else:
                    res += flatten_and_sort(item)
        return res
