import os
os.system("algokit compile py --out-dir ./app app.py")
os.system("algokit generate client app/Eval.arc32.json --output client.py")
import algosdk
import algokit_utils as au
import algokit_utils.transactions.transaction_composer as att

from utils import (
    account_creation,
    display_info,
)

# from app import (
#     claim_algo,
# )

# def box(app_id, box_name):
#     return algorand.app.get_box_value(app_id, box_name=box_name)

if __name__ == "__main__":
    algorand = au.AlgorandClient.testnet()

    algod_client = algorand.client.algod
    indexer_client = algorand.client.indexer

    print(algod_client.block_info(0))
    print(indexer_client.health())

    # alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10000))
    
    # with open(".env", "w") as file:
    #     file.write(algosdk.mnemonic.from_private_key(alice.private_key))
    # bob = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))
    # charly = account_creation(algorand, "CHARLY", au.AlgoAmount(algo=100))
    sy = algorand.account.from_mnemonic(mnemonic='song forest float crane dry sphere swamp define trumpet brick ignore gas salon involve portion hunt lottery apology adjust remind human razor thunder above cup')
    import client as cl
    factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory, default_sender=sy.address
    )
    app_id = 736038676
    ac = factory.get_app_client_by_id(app_id, default_sender=sy.address, default_signer=sy.signer)
    ac.send.claim_algo(
        au.CommonAppCallParams(box_references=[sy.public_key, b"q1" + sy.public_key]),         
    )

    send_params=au.SendParams(populate_app_call_resources=True)

    sp = algorand.get_suggested_params()
    mbr_pay_txn = algorand.create_transaction.payment(
        au.PaymentParams(
            sender=sy.address,
            receiver=ac.app_address,
            amount=au.AlgoAmount(algo=0.2),
            extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
        )
    )

    
    res_asset = algorand.send.asset_create(
        au.AssetCreateParams(
            sender=sy.address,
            signer=sy.signer,
            total=15,
            decimals=0,
            default_frozen=False,
        )
    )

    asset_id = res_asset.confirmation["asset-index"]

    mbr_pay_txn = algorand.create_transaction.payment(
        au.PaymentParams(
            sender=sy.address,
            receiver=ac.app_address,
            amount=au.AlgoAmount(algo=0.2),
            extra_fee=au.AlgoAmount(micro_algo=sp.min_fee),
        )
    )

    result = ac.send.opt_in_to_asset(
        cl.OptInToAssetArgs(
            mbr_pay=att.TransactionWithSigner(
                mbr_pay_txn,
                sy.signer
            ),
            asset=asset_id
        ),
        params=au.CommonAppCallParams(
            box_references=[sy.address],
            sender=sy.address,
            signer=sy.signer,
        ),
        send_params=send_params
    )

    result = ac.send.sum(
        cl.SumArgs(
            array=bytes([1, 2])
        ),
        params=au.CommonAppCallParams(
            box_references=[sy.address],
            sender=sy.address,
            signer=sy.signer,
        ),
        send_params=send_params
    )

    result = ac.send.update_box(
        cl.UpdateBoxArgs(
            value="test"
        ),
        params=au.CommonAppCallParams(
            box_references=[sy.address],
            sender=sy.address,
            signer=sy.signer,
        ),
        send_params=send_params
    )
#     print("Sy Create a Token")
#     result = algorand.send.asset_create(
#         au.AssetCreateParams(
#             sender=alice.address,
#             signer=alice.signer,
#             total=15,
#             decimals=0,
#             default_frozen=False,
#             unit_name="PY-CL-FD",  # 8 Max
#             asset_name="Proof of Attendance Py-Clermont",
#             url="https://pyclermont.org/",
#             note="Hello Clermont",
#         )
#     )
#     asset_id = result.confirmation["asset-index"]

#     print("BOB Buy 1 Token at 10 Algo from Alice\n")

#     composer = algorand.new_group()

#     composer.add_asset_opt_in(
#         au.AssetOptInParams(
#             sender=bob.address,
#             signer=bob.signer,
#             asset_id=asset_id
#         )
#     )
#     composer.add_payment(
#         au.PaymentParams(
#             sender=bob.address,
#             signer=bob.signer,
#             receiver=alice.address,
#             amount=au.AlgoAmount(algo=10),
#         )
#     )
#     composer.add_asset_transfer(
#         au.AssetTransferParams(
#             sender=alice.address,
#             signer=alice.signer,
#             receiver=bob.address,
#             amount=1,
#             asset_id=asset_id,
#         )
#     )

#     result = composer.send()

#     price = au.AlgoAmount(algo=10)

#     display_info(algorand, ["ALICE", "BOB"])

#     print("Alice Create a smart contract")
#     # compile the smart contract

#     os.system("algokit compile py --out-dir ./app app.py")

#     os.system("algokit generate client app/DigitalMarketplace.arc32.json --output client.py")
    # import client as cl

    # factory = algorand.client.get_typed_app_factory(
    #     cl.EvalFactory, default_sender='song forest float crane dry sphere swamp define trumpet brick ignore gas salon involve portion hunt lottery apology adjust remind human razor thunder above cup'
    # )
    
    # result, _ = factory.send.create.create_application(
    #     cl.CreateApplicationArgs(
    #         asset_id=asset_id, unitary_price=price.micro_algo
    #     )
    # )
    # app_id = result.app_id
    # ac = factory.get_app_client_by_id(app_id, default_sender='song forest float crane dry sphere swamp define trumpet brick ignore gas salon involve portion hunt lottery apology adjust remind human razor thunder above cup')
    

#     display_info(algorand, ["ALICE"])
#     print(f"App {app_id} deployed with address {ac.app_address}")

#     sp = algorand.get_suggested_params()

#     mbr_pay_txn = algorand.create_transaction.payment(
#         au.PaymentParams(
#             sender=alice.address,
#             receiver=ac.app_address,
#             amount=au.AlgoAmount(algo=0.2),
#             extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
#         )
#     )

#     ac.send.opt_in_to_asset(
#         cl.OptInToAssetArgs(
#             mbr_pay=att.TransactionWithSigner(mbr_pay_txn, alice.signer)
#         ),
#         send_params=au.SendParams(populate_app_call_resources=True)
#     )

#     print(
#         f"App can now Hold ASA-ID= {
#             algod_client.account_info(ac.app_address)['assets']
#         }"
#     )

#     print("Alice send ASAs to the App")
#     algorand.send.asset_transfer(
#         au.AssetTransferParams(
#             sender=alice.address,
#             signer=alice.signer,
#             amount=10,
#             receiver=ac.app_address,
#             asset_id=asset_id
#         )
#     )
#     print(f"Hold ASA-ID= {algod_client.account_info(ac.app_address)['assets']}")

#     amt_to_buy = 2
#     print(f"Charly buy {amt_to_buy} token")
#     composer = algorand.new_group()
#     composer.add_asset_opt_in(
#         au.AssetOptInParams(
#             sender=charly.address,
#             signer=charly.signer,
#             asset_id=asset_id
#         )
#     )
#     buyer_payment_txn = algorand.create_transaction.payment(
#         au.PaymentParams(
#             sender=charly.address,
#             receiver=ac.app_address,
#             amount=au.AlgoAmount(
#                 micro_algo=amt_to_buy*ac.state.global_state.unitary_price
#             ),
#             extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
#         )
#     )

#     composer.add_app_call_method_call(
#         ac.params.buy(
#             cl.BuyArgs(
#                 buyer_txn=att.TransactionWithSigner(
#                     txn=buyer_payment_txn,
#                     signer=charly.signer
#                 ),
#                 quantity=2,
#             ),
#             au.CommonAppCallParams(
#                 sender=charly.address,
#                 signer=charly.signer,
#             )
#         )
#     )
#     composer.send(au.SendParams(populate_app_call_resources=True))

#     display_info(algorand, ["CHARLY"])

#     print("Alice delete the app and get ASA and Algo back")
#     # Delete the smart contract

#     ac.send.delete.delete_application(
#         au.CommonAppCallParams(
#             # Tell the AVM that the transaction involves this asset
#             asset_references=[asset_id],
#             extra_fee=au.AlgoAmount(micro_algo=2*sp.min_fee)
#         )
#     )

#     display_info(algorand, ["ALICE", "BOB", "CHARLY"])