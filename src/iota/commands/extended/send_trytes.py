# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

from typing import List

import filters as f
from iota import TryteString
from iota.commands import FilterCommand, RequestFilter
from iota.commands.core.attach_to_tangle import AttachToTangleCommand
from iota.commands.core.get_transactions_to_approve import \
  GetTransactionsToApproveCommand
from iota.commands.extended.broadcast_and_store import BroadcastAndStoreCommand
from iota.filters import Trytes

__all__ = [
  'SendTrytesCommand',
]


class SendTrytesCommand(FilterCommand):
  """
  Executes `sendTrytes` extended API command.

  See :py:meth:`iota.api.IotaApi.send_trytes` for more info.
  """
  command = 'sendTrytes'

  def get_request_filter(self):
    return SendTrytesRequestFilter()

  def get_response_filter(self):
    pass

  def _execute(self, request):
    depth                 = request['depth'] # type: int
    min_weight_magnitude  = request['min_weight_magnitude'] # type: int
    trytes                = request['trytes'] # type: List[TryteString]

    # Call ``getTransactionsToApprove`` to locate trunk and branch
    # transactions so that we can attach the bundle to the Tangle.
    gta_response = GetTransactionsToApproveCommand(self.adapter)(depth=depth)

    AttachToTangleCommand(self.adapter)(
      branch_transaction  = gta_response.get('branchTransaction'),
      trunk_transaction   = gta_response.get('trunkTransaction'),

      min_weight_magnitude  = min_weight_magnitude,
      trytes                = trytes,
    )

    return BroadcastAndStoreCommand(self.adapter)(trytes=request['trytes'])


class SendTrytesRequestFilter(RequestFilter):
  def __init__(self):
    super(SendTrytesRequestFilter, self).__init__({
      'depth': f.Required | f.Type(int) | f.Min(1),

      'trytes': f.Required | f.Array | f.FilterRepeater(f.Required | Trytes),

      # Loosely-validated; testnet nodes require a different value than
      # mainnet.
      'min_weight_magnitude': f.Required | f.Type(int) | f.Min(1),
    })