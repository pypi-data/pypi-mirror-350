/*      Compiler: ECL 24.5.10                                         */
/*      Date: 2025/5/24 22:21 (yyyy/mm/dd)                            */
/*      Machine: Darwin 23.6.0 arm64                                  */
/*      Source: /Users/runner/sage-local/var/tmp/sage/build/fricas-1.3.11/src/pre-generated/src/algebra/ACF-.lsp */
#include <ecl/ecl-cmp.h>
#include "/Users/runner/sage-local/var/tmp/sage/build/fricas-1.3.11/src/_build/target/aarch64-apple-darwin23.6.0/algebra/ACF-.eclh"
/*      function definition for ACF-;zeroOf;SupS;1                    */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L679_acf__zeroof_sups_1_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3_x_;
  v3_x_ = ECL_NIL;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[8];
   T0 = _ecl_car(v4);
   T1 = _ecl_cdr(v4);
   v3_x_ = (cl_env_copy->function=T0)->cfun.entry(1, T1);
  }
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[10];
   T1 = _ecl_car(v4);
   T2 = _ecl_cdr(v4);
   T0 = (cl_env_copy->function=T1)->cfun.entry(3, v1_p_, v3_x_, T2);
  }
  value0 = L685_acf__assign_(v3_x_, T0, v2_);
  return value0;
 }
}
/*      function definition for ACF-;rootOf;SupS;2                    */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L680_acf__rootof_sups_2_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3_x_;
  v3_x_ = ECL_NIL;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[8];
   T0 = _ecl_car(v4);
   T1 = _ecl_cdr(v4);
   v3_x_ = (cl_env_copy->function=T0)->cfun.entry(1, T1);
  }
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[12];
   T1 = _ecl_car(v4);
   T2 = _ecl_cdr(v4);
   T0 = (cl_env_copy->function=T1)->cfun.entry(3, v1_p_, v3_x_, T2);
  }
  value0 = L685_acf__assign_(v3_x_, T0, v2_);
  return value0;
 }
}
/*      function definition for ACF-;zerosOf;SupL;3                   */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L681_acf__zerosof_supl_3_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2, T3;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3;
  v3 = (v2_)->vector.self.t[15];
  T0 = _ecl_car(v3);
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[8];
   T2 = _ecl_car(v4);
   T3 = _ecl_cdr(v4);
   T1 = (cl_env_copy->function=T2)->cfun.entry(1, T3);
  }
  T2 = _ecl_cdr(v3);
  value0 = (cl_env_copy->function=T0)->cfun.entry(3, v1_p_, T1, T2);
  return value0;
 }
}
/*      function definition for ACF-;rootsOf;SupL;4                   */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L682_acf__rootsof_supl_4_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2, T3;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3;
  v3 = (v2_)->vector.self.t[17];
  T0 = _ecl_car(v3);
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[8];
   T2 = _ecl_car(v4);
   T3 = _ecl_cdr(v4);
   T1 = (cl_env_copy->function=T2)->cfun.entry(1, T3);
  }
  T2 = _ecl_cdr(v3);
  value0 = (cl_env_copy->function=T0)->cfun.entry(3, v1_p_, T1, T2);
  return value0;
 }
}
/*      function definition for ACF-;rootsOf;SupSL;5                  */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L683_acf__rootsof_supsl_5_(cl_object v1_p_, cl_object v2_y_, cl_object v3_)
{
 cl_object T0;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 T0 = ecl_elt(v3_,12);
 value0 = L692_acf__allroots_(v1_p_, v2_y_, T0, v3_);
 return value0;
}
/*      function definition for ACF-;zerosOf;SupSL;6                  */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L684_acf__zerosof_supsl_6_(cl_object v1_p_, cl_object v2_y_, cl_object v3_)
{
 cl_object T0;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 T0 = ecl_elt(v3_,10);
 value0 = L692_acf__allroots_(v1_p_, v2_y_, T0, v3_);
 return value0;
}
/*      function definition for ACF-;assign                           */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L685_acf__assign_(cl_object v1_x_, cl_object v2_f_, cl_object v3_)
{
 cl_object T0;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 T0 = (v3_)->vector.self.t[6];
 ecl_function_dispatch(cl_env_copy,VV[32])(3, v1_x_, v2_f_, T0) /*  assignSymbol */;
 value0 = v2_f_;
 cl_env_copy->nvalues = 1;
 return value0;
}
/*      function definition for ACF-;zeroOf;PS;8                      */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L686_acf__zeroof_ps_8_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2, T3;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3_l_;
  v3_l_ = ECL_NIL;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[23];
   T0 = _ecl_car(v4);
   T1 = _ecl_cdr(v4);
   v3_l_ = (cl_env_copy->function=T0)->cfun.entry(2, v1_p_, T1);
  }
  if (!(v3_l_==ECL_NIL)) { goto L2; }
  value0 = ecl_function_dispatch(cl_env_copy,VV[34])(1, VV[8]) /*  error */;
  return value0;
L2:;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[10];
   T0 = _ecl_car(v4);
   {
    cl_object v5;
    v5 = (v2_)->vector.self.t[25];
    T2 = _ecl_car(v5);
    T3 = _ecl_cdr(v5);
    T1 = (cl_env_copy->function=T2)->cfun.entry(2, v1_p_, T3);
   }
   if (Null(v3_l_)) { goto L13; }
   T2 = _ecl_car(v3_l_);
   goto L12;
L13:;
   T2 = ecl_function_dispatch(cl_env_copy,VV[35])(0) /*  FIRST_ERROR  */;
L12:;
   T3 = _ecl_cdr(v4);
   value0 = (cl_env_copy->function=T0)->cfun.entry(3, T1, T2, T3);
   return value0;
  }
 }
}
/*      function definition for ACF-;rootOf;PS;9                      */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L687_acf__rootof_ps_9_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2, T3;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3_l_;
  v3_l_ = ECL_NIL;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[23];
   T0 = _ecl_car(v4);
   T1 = _ecl_cdr(v4);
   v3_l_ = (cl_env_copy->function=T0)->cfun.entry(2, v1_p_, T1);
  }
  if (!(v3_l_==ECL_NIL)) { goto L2; }
  value0 = ecl_function_dispatch(cl_env_copy,VV[34])(1, VV[10]) /*  error */;
  return value0;
L2:;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[12];
   T0 = _ecl_car(v4);
   {
    cl_object v5;
    v5 = (v2_)->vector.self.t[25];
    T2 = _ecl_car(v5);
    T3 = _ecl_cdr(v5);
    T1 = (cl_env_copy->function=T2)->cfun.entry(2, v1_p_, T3);
   }
   if (Null(v3_l_)) { goto L13; }
   T2 = _ecl_car(v3_l_);
   goto L12;
L13:;
   T2 = ecl_function_dispatch(cl_env_copy,VV[35])(0) /*  FIRST_ERROR  */;
L12:;
   T3 = _ecl_cdr(v4);
   value0 = (cl_env_copy->function=T0)->cfun.entry(3, T1, T2, T3);
   return value0;
  }
 }
}
/*      function definition for ACF-;zerosOf;PL;10                    */
/*      optimize speed 3, debug 0, space 0, safety 0                  */
static cl_object L688_acf__zerosof_pl_10_(cl_object v1_p_, cl_object v2_)
{
 cl_object T0, T1, T2, T3;
 cl_object env0 = ECL_NIL;
 const cl_env_ptr cl_env_copy = ecl_process_env();
 cl_object value0;
TTL:
 {
  cl_object v3_l_;
  v3_l_ = ECL_NIL;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[23];
   T0 = _ecl_car(v4);
   T1 = _ecl_cdr(v4);
   v3_l_ = (cl_env_copy->function=T0)->cfun.entry(2, v1_p_, T1);
  }
  if (!(v3_l_==ECL_NIL)) { goto L2; }
  value0 = ecl_function_dispatch(cl_env_copy,VV[34])(1, VV[12]) /*  error */;
  return value0;
L2:;
  {
   cl_object v4;
   v4 = (v2_)->vector.self.t[15];
   T0 = _ecl_car(v4);
   {
    cl_object v5;
    v5 = (v2_)->vector.self.t[25];
    T2 = _ecl_car(v5);
    T3 = _ecl_cdr(v5);
    T1 = (cl_env_copy->function=T2)->cfun.entry(2, v1_p_, T3);
   }
   if (Null(v3_l_)) { goto L13; }
   T2 = _ecl_car(v3_l_);
   goto L12;
L13:;
   T2 = ecl_function_dispatch(cl_env_copy,VV[35])(0) /*  FIRST_ERROR  */;
L12:;
   T3 = _ecl_cdr(v4);
   value0 = (cl_env_copy->function=T0)->cfun.entry(3, T1, T2, T3);
   return value0;
  }
 }
}
/*      function definition for ACF-;rootsOf;PL;11                    */