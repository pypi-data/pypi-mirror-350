struct {
  double sig, rxx;
} tv_;

struct {
  double bl, anl, ana;
} leng_;

struct {
  int isig;
} in_;

struct {
  double cab, cnb, cmb;
} base_;

struct {
  double cap, cnp, cmp, hb;
} band_;

struct {
  double cxt[240], cnt[240], cmt[240], cpv[21];
  int ja, jb, kf;
} cvp_;

struct {
  double r1, pi;
  int i9, jh1, kl;
} disc_;

struct {
  double cabl, cnbl, cmbl, caw, cnw, cmw;
} wave_;

struct {
  double cxo, cyo, cmo;
} tail1_;

struct {
  double voln, sobs, rja1, rja2;
  int icount, ngol, nhbs;
} icou_;

struct {
  int nfl, nn, iprint, mal, max, ipr;
} geo2_;

struct {
  double xb[240], rb[240], rbp[240], c2, beta;
} geom1_;

struct {
  double xr[6][20], g[20], gch, dm;
  int n, n1[20], ix, i1;
} rx_;

struct {
  int ntt[11], np5, jzt;
} nni_;

struct {
  double vovs, al, yint, f, rr, rref, aref, dln;
} geo3_;


struct {
  double caf, cnf, cmf, cmx, dia, rn, ap, xp;
} vol_;

struct {
  double preb[10], rab1[10], rab2[10];
  int ipe, npr, nupr;
} preob_;

struct {
  double ainf, rhoinf, amuinf, cts, dl, hmax, dmax, huat, duat, dpr;
  int ng, nh, nk;
} input_data_;
