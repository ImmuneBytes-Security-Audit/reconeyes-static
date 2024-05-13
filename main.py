from termcolor import colored
import runner, impact, informational, optimisational
import pprint

filename = "SimpleStorage.sol"
su, suo, n, name_of_contracts, pragma_value = runner.pipeline(filename)
if su:
      if pragma_value != '0.8.18':
        print(colored("\n[Informational] incorrect-versions-of-solidity. ", "green") + colored(pragma_value + " is not recommended for deployment ", "green"))

      for name in name_of_contracts:
          print("\n\n\n------------- " + name + " -------------\n") 
          try:
              # ----- KNOWN DETECTORS -----
              if pragma_value == "0.4.22":    
                  impact.multiple_constructors(name)
  
              if pragma_value == "0.8.18":
                  informational.deprecated_selfdestruct(name)
              
              val = float(pragma_value.split('0.')[1])
              # print(type(val))
              if val >= 4.7 and val <= 5.9:
                  impact.abiencoderv2_array(name)
              
              if val <=5.0:
                  impact.public_mappings_nested(name)
                  
              impact.uninitialized_state(name)
              impact.boolean_cst(name)
              impact.divide_before_multiply(name)
              impact.uninitialized_local(name)
              optimisational.constable_states(name)
              impact.calls_loop(name)
              informational.block_timestamp(name)
              informational.too_many_digits(name)
              optimisational.costly_loop(name)
              informational.unused_state_variable(name)
              informational.dead_code(name)
              impact.shadowing_builtin(name)
              impact.suicidal(name)
              impact.controlled_array_length(name)
              impact.arbitrary_send_eth(name)
              informational.low_level_calls(name)
              impact.controlled_delegatecall(name)
              impact.incorrect_shift(name)
              informational.assembly(name)
              impact.msg_value(name)
              impact.locked_ether(name)
              impact.weak_prng(name)
              impact.storage_array(name)
              impact.txorigin(name)
              impact.mapping_deletion(name)
              impact.event_maths_access(name)
              impact.missing_zero_check(name)
              impact.assert_state_change(name)
              informational.depracacted_standards(name)
              impact.erc20_interface(name)
              impact.erc721_interface(name)
              informational.erc20_indexed(name)
              impact.domain_separator_collision(name)
              impact.incorrect_equality(name)
              optimisational.external_functions(name)
              impact.void_cst(name)
              impact.missing_inheritance(name)
              informational.unimplemented_function(name)
              impact.arbitrary_send_erc20(name)
              impact.arbitrary_send_erc20_permit(name)
              impact.delegate_call_in_loop(name)
              impact.unchecked_send(name)
              optimisational.immutable_state(name)
              impact.tautology(name)
              impact.incorrect_modifier(name)
              informational.function_init_state(name)
              impact.unchecked_transfer(name)
              informational.naming_convention(name)
              impact.unused_return(name)
  
              # #  ------ CUSTOM DETECTORS -------
              impact.remove_approve(name)
              impact.incorrect_return_interfaces(name)
              impact.denial_of_service(name)
              optimisational.incorrect_use_of_view(name)
          except Exception as e:
              print("An Error Occurred in main.py: ", e)
